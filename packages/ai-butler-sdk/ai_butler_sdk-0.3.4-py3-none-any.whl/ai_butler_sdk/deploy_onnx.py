import os
from ai_butler_sdk.settings import settings
import docker
from ai_butler_sdk.apis.client import update_deploy_task, DeployOnlineInferStatusEnum
from loguru import logger
from ai_butler_sdk.utils import unzip_file, is_port_open
import time
import httpx
import shutil
import traceback


class DeployOnnxInfer:
    """部署onnx推理服务基类"""

    def __init__(self, deploy_task_id, token, train_task_result_url, is_gpu=False, base_dir: str = ""):
        self.deploy_task_id = deploy_task_id
        self.token = token
        self.train_task_result_url = train_task_result_url
        self.onnx_weight_path = os.path.join(
            base_dir, f"output/deploy/{deploy_task_id}/{settings.DEPLOY_ONNX_WEIGHT_DIR}"
        )
        os.makedirs(self.onnx_weight_path, exist_ok=True)
        self.is_gpu = is_gpu
        if is_gpu:
            self.docker_image_name = settings.DEPLOY_ONNX_DOCKER_IMAGE_GPU
        else:
            self.docker_image_name = settings.DEPLOY_ONNX_DOCKER_IMAGE_CPU

    def download_onnx_weight(self):
        logger.info("---------------------------------开始下载权重文件---------------------------------")
        timestamp = str(int(time.time() * 1000))
        with httpx.stream("GET", url=self.train_task_result_url) as resp:
            # 打开本地文件以二进制写模式
            target_path = os.path.join(self.onnx_weight_path, f"{timestamp}.zip")
            with open(target_path, "wb") as f:
                for chunk in resp.iter_bytes():
                    f.write(chunk)
                    # 可选地在这里调用flush来确保数据及时写入磁盘
                    f.flush()
            # 解压文件
            unzip_file(target_path, target_path[:-4])
        os.remove(target_path)  # 删除压缩包
        for dir_path, dirs, files in os.walk(self.onnx_weight_path):
            for file in files:
                # 查找以 .onnx 结尾的文件
                if file.endswith(".onnx"):
                    # 构建完整文件路径
                    src_file_path = os.path.join(dir_path, file)
                    dst_file_path = os.path.join(self.onnx_weight_path, file)
                    # 将文件移动到目标目录
                    shutil.move(src_file_path, dst_file_path)

                if file == "labels.txt":
                    # 构建完整文件路径
                    src_file_path = os.path.join(dir_path, file)
                    dst_file_path = os.path.join(self.onnx_weight_path, file)
                    # 将文件移动到目标目录
                    shutil.move(src_file_path, dst_file_path)
        logger.info("---------------------------------权重文件下载完成---------------------------------")

    def select_port(self) -> int | None:
        # 配置好的可用端口 - 已使用的端口 = 剩余可用端口中随机选择一个
        ports = settings.DEPLOY_ONNX_AVAILABLE_PORT.split(",")
        selected_port = None
        for port in ports:
            if is_port_open(settings.DEPLOY_ONNX_IP_ADDRESS, port):
                continue
            else:
                selected_port = port
                break
        return selected_port

    def docker_run(self, port: int) -> str:
        client = docker.from_env()
        client.images.pull(self.docker_image_name)
        container_id = client.containers.run(
            image=self.docker_image_name,
            detach=True,  # 是否以后台模式运行
            volumes={self.onnx_weight_path: {"bind": f"/srv/app/{settings.DEPLOY_ONNX_WEIGHT_DIR}", "mode": "rw"}},
            ports={"8000/tcp": port},  # 端口映射，这里将容器的80端口映射到主机的8080端口
            name=f"{self.docker_image_name}-{port}",  # 容器名称
        )
        return container_id

    def __call__(self, *args, **kwargs):
        try:
            update_deploy_task(self.deploy_task_id, DeployOnlineInferStatusEnum.DEPLOYING)
            # 下载权重文件
            self.download_onnx_weight()
            # 选择端口号
            port = self.select_port()
            if not port:
                update_deploy_task(self.deploy_task_id, DeployOnlineInferStatusEnum.FAILURE, reason="无可用端口号!")
                return
            # 拉取并启动docker镜像
            container_id = self.docker_run(port)
            # 上报部署结果
        except Exception:
            logger.error(f"部署任务失败: {traceback.format_exc()}")
            update_deploy_task(self.deploy_task_id, DeployOnlineInferStatusEnum.FAILURE, reason=f"error: {e}")
        else:
            address = f"http://{settings.DEPLOY_ONNX_IP_ADDRESS}:{port}"
            update_deploy_task(self.deploy_task_id, DeployOnlineInferStatusEnum.FINISH, address, container_id)
