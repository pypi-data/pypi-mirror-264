import typing as t
from abc import ABC, abstractmethod

class Command(ABC):
    @property
    @abstractmethod
    def description(self) -> str:
        pass

    @abstractmethod
    def command(self, *args, **kwargs) -> t.Any:
        pass
    
    def arg_kwargs_prompt_loop(
        self
    ) -> t.Union[t.Tuple[t.Tuple[t.Any], t.Dict[str, t.Any]], None]:
        return None

    def execute(self):
        print(self.description)
        params = self.arg_kwargs_prompt_loop()
        if not params:
            results = self.command()
        else:
            args, kwargs = params
            results = self.command(*args, **kwargs)
        return self.post_execution(results)
    
    def post_execution(self, results: t.Any):
        print("Finished executing")
