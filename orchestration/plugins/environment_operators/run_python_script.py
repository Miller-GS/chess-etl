from airflow.models.baseoperator import BaseOperator
from environment_operators.strategies import (
    EnvironmentStrategyEnum,
    EnvironmentStrategyFactory,
)


class RunPythonScriptOperator(BaseOperator):
    template_fields = ["strategy_args", "script_path", "script_args"]

    def __init__(
        self,
        strategy: EnvironmentStrategyEnum,
        strategy_args: dict,
        script_path: str,
        script_args: list = None,
        **kwargs
    ) -> None:
        super().__init__(**kwargs)

        self.factory = EnvironmentStrategyFactory()
        self.strategy_type = strategy
        self.strategy_args = strategy_args
        self.script_path = script_path
        self.script_args = script_args

    def execute(self, context):
        strategy = self.factory.create(self.strategy_type, **self.strategy_args)
        strategy.run_python_script(self.script_path, self.script_args)
