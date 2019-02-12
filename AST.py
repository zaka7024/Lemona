
class NodeVisitor:
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))


class AST:
    pass


class Program:

    def __init__(self, statements_list):
        self.statements = statements_list


class Selction:

    def __init__(self, cond, true_statements, false_statements=None):
        self.cond = cond
        self.true_statements = true_statements
        self.false_statements = false_statements


class Repetition:

    def __init__(self, _from, to, statements, step=1):
        self._from = _from
        self._to = to
        self.step = step
        self.statements = statements


class Assignment:

    def __init__(self, token, value):
        self.token = token
        self.id = self.token.value
        self.value = value


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


class ListDec:

    def __init__(self, node):
        self.name = node.name
        self.value = node.value


class List:

    def __init__(self, name, value):
        self.name = name
        self.value = value


class Num:

    def __init__(self, node):
        self.token = node
        self.value = self.token.value

    def __str__(self):
        return "Num object"