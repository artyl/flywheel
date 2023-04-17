import os

from colorama import Fore

from data_level import DataOperations as dop


class UiOperations:
    
    def __init__(self, print_func=None, input_func=None):
        self.print = print if print_func is None else print_func
        self.input = input if print_func is None else input_func
    
    def user_session(self, phrase: str, repetition: dict) -> (float, str):
        """Console user interface"""
        user_input: str = self.input(f'Enter phrase \"{phrase}\" in English: ' + os.linesep)
        distance, best_translation = dop.find_max_string_similarity(user_input, repetition['translations'])
        diff = dop.find_user_mistakes(user_input, best_translation)

        if distance >= dop.level_excellent:  # Phrases are identical
            self.print(Fore.GREEN + 'Correct!' + os.linesep)
        elif distance >= dop.level_good:  # The phrases are very similar, maybe a typo
            self.print(Fore.RESET + 'Almost correct. Right answer is: ', end='')
            self._print_colored_diff(diff, best_translation)
            self.print(os.linesep)
        elif distance >= dop.level_mediocre:  # Phrases have a lot in common
            self.print(Fore.RESET + 'Not bad. Right answer is: ', end='')
            self._print_colored_diff(diff, best_translation)
            self.print(os.linesep)
        else:
            self.print(Fore.RED + 'Wrong. ', end='')  # There are too many errors
            self.print(Fore.RESET + 'Right answer is: ' + Fore.GREEN + best_translation + os.linesep)

        self.print(Fore.RESET, end='')

        return distance, best_translation
    
    def _print_colored_diff(self, correction, reference) -> None:
        """Visualisation of user errors"""
        for i, ch in enumerate(reference):
            if correction[i]:
                self.print(Fore.GREEN + ch, end='')
            else:
                if ch != ' ':
                    self.print(Fore.RED + ch, end='')  # Just a letter
                else:
                    if i - 1 >= 0 and i + 1 < len(reference):  # Emphasise the space between correct but sticky characters
                        if correction[i - 1] and correction[i + 1]:
                            self.print(Fore.RED + '_', end='')
                        else:
                            self.print(Fore.RED + ' ', end='')
