
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


class Cond:

    def __init__(self, left, op, right):
        self.left = left
        self.right = right
        self.type = self.op = op

class CondOp:

    def __init__(self, left, op, right):
        self.type = op.type
        self.op = op
        self.left = left
        self.right = right

class VarDecList:

    def __init__(self):
        self.children = []

class VarDec:

    def __init__(self, node):
        self.name = node.name
        self.value = node.value


class Var:

    def __init__(self, name, value):
        self.name = name
        self.value = value


class Num:

    def __init__(self, node):
        self.token = node
        self.value = self.token.value

    def __str__(self):
        return "Num object"