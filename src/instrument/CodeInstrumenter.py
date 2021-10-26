import libcst as cst
from libcst.metadata import ParentNodeProvider, PositionProvider


class CodeInstrumenter(cst.CSTTransformer):

    METADATA_DEPENDENCIES = (ParentNodeProvider, PositionProvider,)

    def __init__(self, file_path, iids):
        self.file_path = file_path
        self.iids = iids

    def __create_iid(self, node):
        location = self.get_metadata(PositionProvider, node)
        line = location.start.line
        column = location.start.column
        iid = self.iids.new(self.file_path, line, column)
        return iid

    def __create_import(self, name):
        module_name = cst.Attribute(value=cst.Name(value="dynapyt"), attr=cst.Name(value="runtime"))
        fct_name = cst.Name(value=name)
        imp_alias = cst.ImportAlias(name=fct_name)
        imp = cst.ImportFrom(module=module_name, names=[imp_alias])
        stmt = cst.SimpleStatementLine(body=[imp])
        return stmt

    # add import of our runtime library to the file
    def leave_Module(self, original_node, updated_node):
        import_assign = self.__create_import("_assign_")
        import_expr = self.__create_import("_expr_")
        import_binop = self.__create_import("_binop_")
        new_body = [import_assign, import_expr, import_binop, cst.Newline(value='\n')]+list(updated_node.body)
        return updated_node.with_changes(body=new_body)

    def leave_BinaryOperation(self, original_node, updated_node):
        callee_name = cst.Name(value="_binop_")
        iid = self.__create_iid(original_node)
        iid_arg = cst.Arg(value=cst.Integer(value=str(iid)))
        left_arg = cst.Arg(updated_node.left)
        operator_name = type(original_node.operator).__name__
        operator_arg = cst.Arg(cst.SimpleString(value=f'"{operator_name}"'))
        right_arg = cst.Arg(updated_node.right)
        val_arg = cst.Arg(original_node)
        call = cst.Call(func=callee_name, args=[
                        iid_arg, left_arg, operator_arg, right_arg, val_arg])
        return call
    
    def leave_Assign(self, original_node, updated_node):
        callee_name = cst.Name(value="_assign_")
        iid = self.__create_iid(original_node)
        iid_arg = cst.Arg(value=cst.Integer(value=str(iid)))
        targets = list(map(lambda t: cst.Element(value=t.target), original_node.targets))
        left_arg = cst.Arg(value=cst.List(targets))
        right_arg = cst.Arg(original_node.value)
        call = cst.Call(func=callee_name, args=[iid_arg, left_arg, right_arg])
        return updated_node.with_changes(value=call)
    
    def leave_Expr(self, original_node, updated_node):
        callee_name = cst.Name(value="_expr_")
        iid = self.__create_iid(original_node)
        iid_arg = cst.Arg(value=cst.Integer(value=str(iid)))
        val_arg = cst.Arg(original_node)
        call = cst.Call(func=callee_name, args=[iid_arg, val_arg])
        return updated_node.with_changes(value=call)
    
    # def leave_FunctionDef(self, original_node, updated_node):
    #     callee_name = cst.Name(value="_func_entry_")
    #     iid = self.__create_iid(original_node)
    #     iid_arg = cst.Arg(value=cst.Integer(value=str(iid)))
    #     entry_stmt = cst.Call(func=callee_name, args=[iid_arg])
    #     print('!!!', updated_node.body.body, '!!!')
    #     return updated_node.with_changes(body=updated_node.body.with_changes(body=[entry_stmt, cst.Newline(value='\n')]+list(updated_node.body.body)))