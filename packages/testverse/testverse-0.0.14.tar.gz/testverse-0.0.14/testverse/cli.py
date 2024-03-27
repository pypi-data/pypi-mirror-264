from .evaluator import Evaluator

if __name__ == "__main__":
    evaluator_cli = Evaluator(mode="cli")
    evaluator_cli.run()
