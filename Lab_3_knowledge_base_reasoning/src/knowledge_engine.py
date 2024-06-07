from experta import KnowledgeEngine, DefFacts, Rule, AND, MATCH, TEST, FORALL, OR
from utils import TerminalColors
from knowledge_base import Problems, Symptoms, Actions, Problem, Cause, Solution, CauseStatus, symptom_to_action_map

class CoffeeMachineExpert(KnowledgeEngine):
    @DefFacts()
    def init(self):
        for symptom in Symptoms:
            yield Cause(description=symptom.value, status=CauseStatus.IRRELEVANT)


    @Rule(Cause(description=MATCH.description, status=CauseStatus.INVESTIGATING))
    def ask_cause(self, description):
        response = input(f"{description} ({TerminalColors.RED}y{TerminalColors.RESET}/{TerminalColors.GREEN}n{TerminalColors.RESET}): ").strip().lower()
        status = CauseStatus.CONFIRMED if response == 'y' else CauseStatus.DENIED
        self.declare(Cause(description=description, status=status))


    @Rule(OR(Problem(description=Problems.HOT_WATER_OR_STEAM.value),
             Problem(description=Problems.COFFEE_DROPS.value),
             AND(Problem(description=Problems.MILK_FROTH_WEAK.value),
                 Cause(description=Symptoms.INAPPROPRIATE_MILK.value, status=CauseStatus.DENIED))))
    def check_system_calcification(self):
        self.declare(Cause(description=Symptoms.SYSTEM_CALCIFICATION.value, status=CauseStatus.INVESTIGATING))

    
    @Rule(OR(Problem(description=Problems.MILK_FROTH_WEAK.value),
             AND(Problem(description=Problems.HOT_WATER_OR_STEAM.value),
                 Cause(description=Symptoms.SYSTEM_CALCIFICATION.value, status=CauseStatus.DENIED))))
    def check_spumatore_clogged(self):
        self.declare(Cause(description=Symptoms.SPUMATORE_CLOGGED.value, status=CauseStatus.INVESTIGATING))

    
    @Rule(AND(Problem(description=Problems.MILK_FROTH_WEAK.value),
              Cause(description=Symptoms.SPUMATORE_CLOGGED.value, status=CauseStatus.DENIED)))
    def check_inappropriate_milk(self):
        self.declare(Cause(description=Symptoms.INAPPROPRIATE_MILK.value, status=CauseStatus.INVESTIGATING))

    
    @Rule(AND(Problem(description=Problems.COFFEE_DROPS.value),
              Cause(description=Symptoms.SYSTEM_CALCIFICATION.value, status=CauseStatus.DENIED)))
    def check_inappropriate_grind_size(self):
        self.declare(Cause(description=Symptoms.INAPPROPRIATE_GRIND_SIZE.value, status=CauseStatus.INVESTIGATING))


    @Rule(AND(Problem(description=Problems.COFFEE_DROPS.value),
              Cause(description=Symptoms.INAPPROPRIATE_GRIND_SIZE.value, status=CauseStatus.DENIED)))
    def check_coffee_too_fine(self):
        self.declare(Cause(description=Symptoms.COFFEE_TOO_FINE.value, status=CauseStatus.INVESTIGATING))


    @Rule(AND(Problem(description=Problems.COFFEE_DROPS.value),
              Cause(description=Symptoms.COFFEE_TOO_FINE.value, status=CauseStatus.DENIED)))
    def check_too_much_coffee(self):
        self.declare(Cause(description=Symptoms.TOO_MUCH_COFFEE.value, status=CauseStatus.INVESTIGATING))


    @Rule(OR(Problem(description=Problems.NO_CREMA.value),
             AND(Problem(description=Problems.COFFEE_DROPS.value),
                 Cause(description=Symptoms.TOO_MUCH_COFFEE.value, status=CauseStatus.DENIED))))
    def check_brewing_unit_clogged(self):
        self.declare(Cause(description=Symptoms.BREWING_UNIT_CLOGGED.value, status=CauseStatus.INVESTIGATING))


    @Rule(AND(Problem(description=Problems.NO_CREMA.value),
              Cause(description=Symptoms.BREWING_UNIT_CLOGGED.value, status=CauseStatus.DENIED)))
    def check_inappropriate_coffee_beans(self):
        self.declare(Cause(description=Symptoms.INAPPROPRIATE_COFFEE_BEANS.value, status=CauseStatus.INVESTIGATING))


    @Rule(AND(Problem(description=Problems.NO_CREMA.value),
              Cause(description=Symptoms.INAPPROPRIATE_COFFEE_BEANS.value, status=CauseStatus.DENIED)))
    def check_old_coffee_beans(self):
        self.declare(Cause(description=Symptoms.OLD_COFFEE_BEANS.value, status=CauseStatus.INVESTIGATING))


    @Rule(Problem(description=Problems.LOUD_GRINDER_NOISE.value))
    def check_grind_size_for_noise(self):
        self.declare(Cause(description=Symptoms.NOT_ADJUSTED_GRIND_SIZE.value, status=CauseStatus.INVESTIGATING))


    @Rule(AND(Problem(description=Problems.LOUD_GRINDER_NOISE.value),
              Cause(description=Symptoms.NOT_ADJUSTED_GRIND_SIZE.value, status=CauseStatus.DENIED)))
    def check_foreign_objects(self):
        self.declare(Cause(description=Symptoms.FOREIGN_OBJECTS.value, status=CauseStatus.INVESTIGATING))


    @Rule(Problem(description=Problems.ERROR_MESSAGE.value))
    def check_brewing_unit_position(self):
        self.declare(Cause(description=Symptoms.BREWING_UNIT_POSITION_INCORRECT.value, status=CauseStatus.INVESTIGATING))


    @Rule(
        FORALL(
            Cause(is_present=MATCH.status),
            TEST(lambda status: status in [CauseStatus.IRRELEVANT.value, CauseStatus.DENIED.value])
        )
    )
    def diagnose_unknown_issue(self):
        self.declare(Solution(action=Actions.CONTACT_SERVICE.value))

    @Rule(Solution(action=MATCH.action))
    def implement_action(self, action):
        print(f"\n{TerminalColors.GREEN}Solution:{TerminalColors.RESET} {action}")
        self.halt()


    @Rule(Cause(description=MATCH.description, status=CauseStatus.CONFIRMED))
    def diagnose_solution(self, description):
        print(f"\n{TerminalColors.YELLOW}Detected cause{TerminalColors.RESET}: {description[:-1].split(' ', 1)[1]}")
        self.declare(Solution(action=symptom_to_action_map[description]))