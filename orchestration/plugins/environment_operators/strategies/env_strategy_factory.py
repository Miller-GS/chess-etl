from environment_operators.strategies.env_strategy_enum import EnvironmentStrategyEnum
from environment_operators.strategies.env_strategy import EnvironmentStrategy
from environment_operators.strategies.sibling_docker_env_strategy import SiblingDockerEnvStrategy

class EnvironmentStrategyFactory:
    STRATEGIES = {
        EnvironmentStrategyEnum.SIBLING_DOCKER: SiblingDockerEnvStrategy
    }

    def create(self, strategy: EnvironmentStrategyEnum, **kwargs) -> EnvironmentStrategy:
        if strategy not in self.STRATEGIES:
            raise Exception(f"Strategy {strategy} not found.")
        
        return self.STRATEGIES[strategy](**kwargs)
