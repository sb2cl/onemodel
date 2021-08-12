import tatsu
from tatsu.walkers import NodeWalker


class CalcWalker(NodeWalker):
    def walk_object(self, node):
        return node

    def walk__add(self, node):
        return self.walk(node.left) + self.walk(node.right)

    def walk__subtract(self, node):
        return self.walk(node.left) - self.walk(node.right)

    def walk__multiply(self, node):
        return self.walk(node.left) * self.walk(node.right)

    def walk__divide(self, node):
        return self.walk(node.left) / self.walk(node.right)


def parse_and_walk_model():
    with open('calc_model.ebnf') as f:
        grammar = f.read()

    parser = tatsu.compile(grammar, asmodel=True)
    model = parser.parse('3')

    print('# WALKER RESULT IS:')
    print(CalcWalker().walk(model))
    print()


if __name__ == '__main__':
    parse_and_walk_model()
