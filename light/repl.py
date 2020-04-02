from parser import parse_source
from evaluator import Evaluator, Environment

py_eval = eval


class Repl:
    def __init__(self):
        self.parse = parse_source
        self.evaluator = Evaluator()
        self.env = Environment()

    def eval(self, ast):
        return self.evaluator.eval(ast[0], self.env)

    def start(self):
        while True:
            print(">>>", end=" ")
            try:
                line = str(input()).strip()
                if line == "":
                    continue
                ast = self.parse(line)

                val = self.eval(ast)
                if val is not None:
                    print(val)
            except KeyboardInterrupt:
                print("\nThank You")
                exit()
            except Exception as e:
                print(e)


if __name__ == '__main__':
    r = Repl()
    r.start()
