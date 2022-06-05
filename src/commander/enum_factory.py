from enum import Enum, auto

class AdventureOptions(Enum):
    VERB = auto()
    NOUN = auto()
    ProperNoun = auto()
    ADJ = auto()
    quit = None
    
    pass

class PrintColors(Enum):
    system = 'red'
    error = 'red'
    error_on = 'on_yellow'
    test = 'green'
    feedback = 'green'
    system_prompt_text = 'grey'
    system_prompt_on = 'on_white'

if __name__ == '__main__':
    print(PrintColors('red'))
    print(AdventureOptions(1).name)
    a = AdventureOptions.NOUN
    print((a, a.name))
    print(PrintColors.system.value)