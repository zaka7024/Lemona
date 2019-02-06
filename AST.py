
class NodeVisitor:
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))


class AST:
    pass


class BinOp:

    def __init__(self, op, left, right):
        self.type = op.type
        self.op = self.token = op
        self.left = left
        self.right = right


class Num:

    def __init__(self, node):
        self.token = node
        self.value = self.token.value
