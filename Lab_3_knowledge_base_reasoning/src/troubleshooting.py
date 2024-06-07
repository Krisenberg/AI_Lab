from utils import TerminalColors
from knowledge_base import Problems, Problem
from knowledge_engine import CoffeeMachineExpert

def check_user_satisfaction():
    question_part_1 = "\nAre you satisfied with the provided solution and want to exit the troubleshooting assistant? "
    question_part_2 = f"({TerminalColors.GREEN}y{TerminalColors.RESET}/{TerminalColors.RED}n{TerminalColors.RESET}): "
    response = input(question_part_1 + question_part_2).strip().lower()
    return response == 'y'

def start_troubleshooting(engine):
    while(True):
        problems = {
            1: Problems.HOT_WATER_OR_STEAM.value,
            2: Problems.MILK_FROTH_WEAK.value,
            3: Problems.COFFEE_DROPS.value,
            4: Problems.NO_CREMA.value,
            5: Problems.LOUD_GRINDER_NOISE.value,
            6: Problems.ERROR_MESSAGE.value
        }

        print("Choose the problem:")
        for key, value in problems.items():
            print(f"{TerminalColors.YELLOW}[{key}]{TerminalColors.RESET} {value}")
        problem_choice = int(input("\nEnter the number of the problem: "))
        print()
        problem_description = problems[problem_choice]
        engine.reset()
        engine.declare(Problem(description=problem_description))
        engine.run()
        if check_user_satisfaction():
            return

if __name__ == "__main__":
    engine = CoffeeMachineExpert()
    start_troubleshooting(engine)