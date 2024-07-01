from dynapyt.analyses.BaseAnalysis import BaseAnalysis
from typing import Callable, Tuple, Dict, Any

class TestAnalysis(BaseAnalysis):
    def begin_execution(self) -> None:
        print("begin execution")

    def enter_with(self, dyn_ast: str, iid: int, func, args):
        print(f"with statement entered")

    def exit_with(self, dyn_ast: str, iid: int, is_suppressed: bool, exc_value):
        print(f"with statement exited")
        
    def runtime_event(self, dyn_ast: str, iid: int) -> None:
        print("runtime event")

    def control_flow_event(self, dyn_ast: str, iid: int) -> None:
        print("control flow event")

    def pre_call(
        self, dyn_ast: str, iid: int, function: Callable, pos_args: Tuple, kw_args: Dict
    ):
        print("pre call: ", function.__name__)


    def post_call(
        self,
        dyn_ast: str,
        iid: int,
        result: Any,
        function: Callable,
        pos_args: Tuple,
        kw_args: Dict,
    ) -> Any:
        print("post call: ", function.__name__)
        
    def end_execution(self) -> None:
        print("end execution")