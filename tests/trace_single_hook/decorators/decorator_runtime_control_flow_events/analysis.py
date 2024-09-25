from dynapyt.analyses.BaseAnalysis import BaseAnalysis


class TestAnalysis(BaseAnalysis):
    def begin_execution(self) -> None:
        print("begin execution")

    def enter_decorator(self, dyn_ast: str, iid: int, decorator: str, args, kwargs) -> None:
        print("enter decorator: ", decorator)

    def exit_decorator(self, dyn_ast: str, iid: int, decorator: str, result, args, kwargs) -> None:
        print("exit decorator: ", decorator)
        
    def runtime_event(self, dyn_ast: str, iid: int) -> None:
        print("runtime event")

    def control_flow_event(self, dyn_ast: str, iid: int) -> None:
        print("control flow event")
        
    def end_execution(self) -> None:
        print("end execution")