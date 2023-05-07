from airflow.models.baseoperator import BaseOperator
from environment_operators.strategies import EnvironmentStrategyEnum, EnvironmentStrategyFactory

class StopEnvironmentOperator(BaseOperator):
    template_fields = ['strategy_args']

    def __init__(self, strategy: EnvironmentStrategyEnum, strategy_args: dict, **kwargs) -> None:
        super().__init__(**kwargs)
        
        self.factory = EnvironmentStrategyFactory()
        self.strategy_type = strategy
        self.strategy_args = strategy_args

    def execute(self, context):
        strategy = self.factory.create(self.strategy_type, **self.strategy_args)
        strategy.stop()
