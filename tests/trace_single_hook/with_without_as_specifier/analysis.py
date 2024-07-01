from dynapyt.analyses.BaseAnalysis import BaseAnalysis
from typing import Any, Callable, Dict, Tuple

class TestAnalysis(BaseAnalysis):
    def begin_execution(self) -> None:
        print("begin execution")

    def enter_with(self, dyn_ast: str, iid: int, func, args):
        print(f"with statement entered")

    def exit_with(self, dyn_ast: str, iid: int, is_suppressed: bool, exc_value):
        print(f"with statement exited")
        
    def end_execution(self) -> None:
        print("end execution")