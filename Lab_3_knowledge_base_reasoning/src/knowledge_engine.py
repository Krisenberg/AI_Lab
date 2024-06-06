from experta import KnowledgeEngine, DefFacts, Rule, AND, MATCH, TEST, FORALL
from utils import TerminalColors
from knowledge_base import Problems, Symptoms, Actions, Problem, Cause, Solution, CauseStatus

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

    @Rule(Problem(description=Problems.HOT_WATER_OR_STEAM.value))
    def check_system_calcification(self):
        self.declare(Cause(description=Symptoms.SYSTEM_CALCIFICATION.value, status=CauseStatus.INVESTIGATING))

    @Rule(AND(Problem(description=Problems.HOT_WATER_OR_STEAM.value),
              Cause(description=Symptoms.SYSTEM_CALCIFICATION.value, status=CauseStatus.CONFIRMED)))
    def diagnose_system_calcification(self):
        self.declare(Solution(action=Actions.DESCALE_SYSTEM.value))

    @Rule(Problem(description=Problems.MILK_FROTH_WEAK.value))
    def check_spumatore_clogged(self):
        self.declare(Cause(description=Symptoms.SPUMATORE_CLOGGED.value, status=CauseStatus.INVESTIGATING))

    @Rule(AND(Problem(description=Problems.MILK_FROTH_WEAK.value),
              Cause(description=Symptoms.SPUMATORE_CLOGGED.value, status=CauseStatus.CONFIRMED)))
    def diagnose_spumatore_clogged(self):
        self.declare(Solution(action=Actions.CLEAN_SPUMATORE.value))

    @Rule(AND(Problem(description=Problems.MILK_FROTH_WEAK.value),
              Cause(description=Symptoms.SPUMATORE_CLOGGED.value, status=CauseStatus.DENIED)))
    def check_inappropriate_milk(self):
        self.declare(Cause(description=Symptoms.INAPPROPRIATE_MILK.value, status=CauseStatus.INVESTIGATING))

    @Rule(AND(Problem(description=Problems.MILK_FROTH_WEAK.value),
              Cause(description=Symptoms.SPUMATORE_CLOGGED.value, status=CauseStatus.DENIED),
              Cause(description=Symptoms.INAPPROPRIATE_MILK.value, status=CauseStatus.CONFIRMED)))
    def diagnose_inappropriate_milk(self):
        self.declare(Solution(action=Actions.USE_COLD_MILK.value))

    @Rule(Problem(description=Problems.COFFEE_DROPS.value))
    def check_system_calcification_for_drops(self):
        self.declare(Cause(description=Symptoms.SYSTEM_CALCIFICATION.value, status=CauseStatus.INVESTIGATING))

    @Rule(AND(Problem(description=Problems.COFFEE_DROPS.value),
              Cause(description=Symptoms.SYSTEM_CALCIFICATION.value, status=CauseStatus.CONFIRMED)))
    def diagnose_system_calcification_for_drops(self):
        self.declare(Solution(action=Actions.DESCALE_SYSTEM.value))

    @Rule(AND(Problem(description=Problems.COFFEE_DROPS.value),
              Cause(description=Symptoms.SYSTEM_CALCIFICATION.value, status=CauseStatus.DENIED)))
    def check_INAPPROPRIATE_GRIND_SIZE(self):
        self.declare(Cause(description=Symptoms.INAPPROPRIATE_GRIND_SIZE.value, status=CauseStatus.INVESTIGATING))

    @Rule(AND(Problem(description=Problems.COFFEE_DROPS.value),
              Cause(description=Symptoms.INAPPROPRIATE_GRIND_SIZE.value, status=CauseStatus.CONFIRMED)))
    def diagnose_INAPPROPRIATE_GRIND_SIZE(self):
        self.declare(Solution(action=Actions.SET_PROPER_GRIND_SIZE.value))

    @Rule(AND(Problem(description=Problems.COFFEE_DROPS.value),
              Cause(description=Symptoms.INAPPROPRIATE_GRIND_SIZE.value, status=CauseStatus.DENIED)))
    def check_coffee_too_fine(self):
        self.declare(Cause(description=Symptoms.COFFEE_TOO_FINE.value, status=CauseStatus.INVESTIGATING))

    @Rule(AND(Problem(description=Problems.COFFEE_DROPS.value),
              Cause(description=Symptoms.COFFEE_TOO_FINE.value, status=CauseStatus.CONFIRMED)))
    def diagnose_coffee_too_fine(self):
        self.declare(Solution(action=Actions.USE_COARSER_GROUND_COFFEE.value))

    @Rule(AND(Problem(description=Problems.COFFEE_DROPS.value),
              Cause(description=Symptoms.COFFEE_TOO_FINE.value, status=CauseStatus.DENIED)))
    def check_too_much_coffee(self):
        self.declare(Cause(description=Symptoms.TOO_MUCH_COFFEE.value, status=CauseStatus.INVESTIGATING))

    @Rule(AND(Problem(description=Problems.COFFEE_DROPS.value),
              Cause(description=Symptoms.TOO_MUCH_COFFEE.value, status=CauseStatus.CONFIRMED)))
    def diagnose_too_much_coffee(self):
        self.declare(Solution(action=Actions.USE_LESS_GROUND_COFFEE.value))

    @Rule(Problem(description=Problems.NO_CREMA.value))
    def check_brewing_unit_clogged_for_crema(self):
        self.declare(Cause(description=Symptoms.BREWING_UNIT_CLOGGED.value, status=CauseStatus.INVESTIGATING))

    @Rule(AND(Problem(description=Problems.NO_CREMA.value),
              Cause(description=Symptoms.BREWING_UNIT_CLOGGED.value, status=CauseStatus.CONFIRMED)))
    def diagnose_no_crema_brewing_unit_clogged(self):
        self.declare(Solution(action=Actions.CLEAN_BREWING_UNIT.value))

    @Rule(AND(Problem(description=Problems.NO_CREMA.value),
              Cause(description=Symptoms.BREWING_UNIT_CLOGGED.value, status=CauseStatus.DENIED)))
    def check_inappropriate_coffee_beans(self):
        self.declare(Cause(description=Symptoms.INAPPROPRIATE_COFFEE_BEANS.value, status=CauseStatus.INVESTIGATING))

    @Rule(AND(Problem(description=Problems.NO_CREMA.value),
              Cause(description=Symptoms.INAPPROPRIATE_COFFEE_BEANS.value, status=CauseStatus.CONFIRMED)))
    def diagnose_inappropriate_coffee_beans(self):
        self.declare(Solution(action=Actions.CHANGE_COFFEE_BEANS.value))

    @Rule(AND(Problem(description=Problems.NO_CREMA.value),
              Cause(description=Symptoms.INAPPROPRIATE_COFFEE_BEANS.value, status=CauseStatus.DENIED)))
    def check_old_coffee_beans(self):
        self.declare(Cause(description=Symptoms.OLD_COFFEE_BEANS.value, status=CauseStatus.INVESTIGATING))

    @Rule(AND(Problem(description=Problems.NO_CREMA.value),
              Cause(description=Symptoms.OLD_COFFEE_BEANS.value, status=CauseStatus.CONFIRMED)))
    def diagnose_old_coffee_beans(self):
        self.declare(Solution(action=Actions.USE_FRESH_COFFEE_BEANS.value))

    @Rule(Problem(description=Problems.LOUD_GRINDER_NOISE.value))
    def check_grind_size_for_noise(self):
        self.declare(Cause(description=Symptoms.INAPPROPRIATE_GRIND_SIZE.value, status=CauseStatus.INVESTIGATING))

    @Rule(AND(Problem(description=Problems.LOUD_GRINDER_NOISE.value),
              Cause(description=Symptoms.INAPPROPRIATE_GRIND_SIZE.value, status=CauseStatus.CONFIRMED)))
    def diagnose_grind_size_not_adjusted(self):
        self.declare(Solution(action=Actions.OPTIMIZE_GRIND_SIZE.value))

    @Rule(AND(Problem(description=Problems.LOUD_GRINDER_NOISE.value),
              Cause(description=Symptoms.INAPPROPRIATE_GRIND_SIZE.value, status=CauseStatus.DENIED)))
    def check_foreign_objects(self):
        self.declare(Cause(description=Symptoms.FOREIGN_OBJECTS.value, status=CauseStatus.INVESTIGATING))

    @Rule(AND(Problem(description=Problems.LOUD_GRINDER_NOISE.value),
              Cause(description=Symptoms.FOREIGN_OBJECTS.value, status=CauseStatus.CONFIRMED)))
    def diagnose_foreign_objects_in_grinder(self):
        self.declare(Solution(action=Actions.REMOVE_FOREIGN_OBJECTS.value))

    @Rule(Problem(description=Problems.ERROR_MESSAGE.value))
    def check_brewing_unit_position(self):
        self.declare(Cause(description=Symptoms.BREWING_UNIT_POSITION_INCORRECT.value, status=CauseStatus.INVESTIGATING))

    @Rule(AND(Problem(description=Problems.ERROR_MESSAGE.value),
              Cause(description=Symptoms.BREWING_UNIT_POSITION_INCORRECT.value, status=CauseStatus.CONFIRMED)))
    def diagnose_brewing_unit_position_incorrect(self):
        self.declare(Solution(action=Actions.RESET_BREWING_UNIT.value))

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
    def print_cause(self, description):
        print(f"\n{TerminalColors.YELLOW}Detected cause{TerminalColors.RESET}: {description}")