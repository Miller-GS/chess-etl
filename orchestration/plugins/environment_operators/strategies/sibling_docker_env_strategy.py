import subprocess
from environment_operators.strategies.env_strategy import EnvironmentStrategy

class SiblingDockerEnvStrategy(EnvironmentStrategy):
    def __init__(
            self,
            container_name: str,
            docker_file_path:str = None,
            image_name: str = None,
            volumes: dict = None,
        ) -> None:
        self.docker_file_path = docker_file_path
        self.image_name = image_name
        self.container_name = container_name
        if volumes is None:
            self.volumes = {}
        else:
            self.volumes = volumes

    def start(self):
        build_process = subprocess.run(
            ["docker", "build", "-t", self.image_name, self.docker_file_path],
            capture_output=True
        )
        if build_process.returncode != 0:
            raise Exception(f"Failed to build image.\nstdout: {build_process.stdout},\nstderr: {build_process.stderr}")
        
        subprocess.run(["docker", "stop", self.container_name])

        run_command = ["docker", "run", "--privileged", "-dit", "--name", self.container_name, "--rm"]
        for host_path, container_path in self.volumes.items():
            run_command.extend(["-v", f"\"{host_path}:{container_path}\""])
        run_command.append(self.image_name)

        # This join appears to be necessary for Windows. Passing a list has a different behavior from passing a string.
        run_process = subprocess.run(" ".join(run_command), capture_output=True, shell=True)

        if run_process.returncode != 0:
            raise Exception(f"Failed to start container.\nstdout: {run_process.stdout},\nstderr: {run_process.stderr}")

    def run_command(self, command: str):
        run_process = subprocess.run(
            ["docker", "exec", self.container_name, "bash", "-c", command],
            capture_output=True
        )
        if run_process.returncode != 0:
            raise Exception(f"Failed to run command.\nstdout: {run_process.stdout},\nstderr: {run_process.stderr}")

    def run_python_script(self, script_path: str, script_args: list = None):
        run_process = subprocess.run(
            ["docker", "exec", self.container_name, "python", script_path, *script_args],
            capture_output=True
        )
        if run_process.returncode != 0:
            raise Exception(f"Failed to run python script.\nstdout: {run_process.stdout},\nstderr: {run_process.stderr}")

    def stop(self):
        subprocess.run(["docker", "stop", self.container_name])
        subprocess.run(["docker", "rm", self.container_name])
