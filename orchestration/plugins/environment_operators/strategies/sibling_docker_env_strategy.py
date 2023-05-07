import subprocess
from .env_strategy import EnvironmentStrategy

class SiblingDockerEnvStrategy(EnvironmentStrategy):
    def __init__(self, container_name: str, docker_file_path:str = None, image_name: str = None) -> None:
        self.docker_file_path = docker_file_path
        self.image_name = image_name
        self.container_name = container_name

    def start(self):
        build_process = subprocess.run(
            ["docker", "build", "-t", self.image_name, self.docker_file_path],
            capture_output=True
        )
        if build_process.returncode != 0:
            raise Exception(f"Failed to build image.\nstdout: {build_process.stdout},\nstderr: {build_process.stderr}")
        
        subprocess.run(["docker", "stop", self.container_name])
        
        run_process = subprocess.run(
            [
                "docker", "run", "-dit", "--name", self.container_name, "--rm", self.image_name
            ],
            capture_output=True
        )

        if run_process.returncode != 0:
            raise Exception(f"Failed to start container.\nstdout: {run_process.stdout},\nstderr: {run_process.stderr}")

    def stop(self):
        subprocess.run(["docker", "stop", self.container_name])
        subprocess.run(["docker", "rm", self.container_name])
