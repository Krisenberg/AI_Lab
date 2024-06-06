from enum import Enum
from experta import Fact, Field

class Problems(Enum):
    HOT_WATER_OR_STEAM = "Hot water or steam generation impossible"
    MILK_FROTH_WEAK = "Milk froth is too weak or no milk froth"
    COFFEE_DROPS = "Coffee flows only drop by drop"
    NO_CREMA = "No crema on the coffee"
    LOUD_GRINDER_NOISE = "Loud grinder noise"
    ERROR_MESSAGE = "Error message on display 'Error 8 service call'"

class Symptoms(Enum):
    SYSTEM_CALCIFICATION = "Is system scaled?"
    SPUMATORE_CLOGGED = "Is spumatore clogged?"
    INAPPROPRIATE_MILK = "Is provided milk inappropriate (NOT fresh and cold)?"
    INAPPROPRIATE_GRIND_SIZE = "Is grind size inappropriate (too fine or too coarse)?"
    COFFEE_TOO_FINE = "Is ground coffee very fine [if used]?"
    TOO_MUCH_COFFEE = "Is added too much ground coffee [if used]?"
    BREWING_UNIT_CLOGGED = "Is brewing unit clogged?"
    FOREIGN_OBJECTS = "Are foreign objects in grinder?"
    BREWING_UNIT_POSITION_INCORRECT = "Is brewing unit positioned incorrectly?"
    OLD_COFFEE_BEANS = "Are coffee beans NOT freshly roasted?"
    INAPPROPRIATE_COFFEE_BEANS = "Is type of coffee beans inappropriate?"

class Actions(Enum):
    DESCALE_SYSTEM = "Descale the system with a high dose of descaling agent"
    CLEAN_SPUMATORE = "Thoroughly clean the spumatore, disassemble it completely"
    USE_COLD_MILK = "Use cold milk"
    SET_PROPER_GRIND_SIZE = "Set a coarser/finer grind size"
    USE_COARSER_GROUND_COFFEE = "Use coarser ground coffee"
    USE_LESS_GROUND_COFFEE = "Use less ground coffee"
    CLEAN_BREWING_UNIT = "Remove and clean the brewing unit"
    OPTIMIZE_GRIND_SIZE = "Optimize the grind size"
    REMOVE_FOREIGN_OBJECTS = "Remove the foreign objects or contact service"
    RESET_BREWING_UNIT = "Turn off the device and remove the plug. Reinsert the plug and turn on the device. When ready, remove and clean the brewing unit"
    USE_FRESH_COFFEE_BEANS = "Use freshly roasted coffee beans"
    CHANGE_COFFEE_BEANS = "Change the type of coffee beans"
    CONTACT_SERVICE = "Seems like a bigger issue - please contact professional service"

class CauseStatus(Enum):
    IRRELEVANT = 0
    INVESTIGATING = 1
    CONFIRMED = 2
    DENIED = 3

class Problem(Fact):
    """Represents a specific problem with the coffee machine"""
    pass

class Cause(Fact):
    """Represents a cause of a problem"""
    status = Field(CauseStatus, default=CauseStatus.IRRELEVANT)

class Solution(Fact):
    """Represents an action that shall be taken to solve a problem"""
    pass