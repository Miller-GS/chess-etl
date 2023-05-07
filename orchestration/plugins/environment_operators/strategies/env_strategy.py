from abc import ABC, abstractmethod

class EnvironmentStrategy(ABC):
    @abstractmethod
    def __init__(self, **kwargs) -> None:
        pass

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def run_command(self, command: str):
        pass

    @abstractmethod
    def run_python_script(self, script_path: str, script_args: list = None):
        pass

    @abstractmethod
    def stop(self):
        pass