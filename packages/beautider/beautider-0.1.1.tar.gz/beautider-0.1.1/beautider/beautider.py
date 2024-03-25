import os

import colorama
from colorama import Fore
import time

colorama.init()

__all__ = ['Loader', 'base']
__author__ = "Bolgaro4ka <https://github.com/bolgaro4ka>"
__date__ = "24 March 2024"

class Loader():
    def __init__(self, size=2.0, colors=True, description='', complete_symbol='█', uncomplete_symbol='·', borders='[]',
                 units='%', min_value=0, max_value=100, show_of=False, show_speed=False):
        if size < 0:
            raise Exception("Size too small")
        if min_value < 0:
            raise Exception("Min value too small")
        if min_value > max_value:
            raise Exception("min_value > max_value - nice")
        self.persent = min_value
        self.size = size
        self.colors = colors
        self.description = description
        self.complete_symbol = complete_symbol
        self.uncomplete_symbol = uncomplete_symbol
        self.left_border = borders[0]
        self.right_border = borders[-1]
        self.units = units
        self.max_value = max_value
        self.min_value = min_value
        self.show_of = show_of
        self.show_speed = show_speed

    def update(self, per: int):
        try:
            test = per + 1
        except TypeError:
            raise Exception("This var only int or bool")

        self.persent = self.persent + per
        if self.persent > self.max_value:
            self.persent = self.max_value
        if self.persent <= self.min_value:
            self.persent = self.min_value

    def _delta_time(self):
        try:
            self.list_per_second.append(self.persent)
        except:
            self.list_per_second = []
            self.start = time.time()
        self.list_per_second.append(self.persent)
        if time.time()-self.start:
            return round(len(self.list_per_second)/(time.time()-self.start), 3)

    @staticmethod
    def example():
        print("""Code: 
        import time
        load = Loader(description='Loading program', show_speed=True, size=801, max_value=100000, show_of=True,
                      units='bytes')
        for _ in range(1, 100001):
            load.update(1)
            time.sleep(0.001)
            load.pr_load()')\nResult: """)
        import time
        load = Loader(description='Loading program', show_speed=True, size=801, max_value=100000, show_of=True,
                      units='bytes')
        for _ in range(1, 100001):
            load.update(1)
            time.sleep(0.001)
            load.pr_load()
    """
    Please use this method instead of print()
    """
    def pr_load(self):
        print('\r', self.__str__(), end='')

    @staticmethod
    def _min_int(num):
        return int(num) if num == int(num) else int(num) + 1

    def __str__(self):

        additional = None
        if self.persent <= self.max_value//5:
            additional = Fore.RED
        elif self.persent <= self.max_value//2:
            additional = Fore.YELLOW
        else:
            additional = Fore.GREEN

        if not self.colors:
            additional=''


        return (additional) + '\r'+ self.left_border + self.complete_symbol * (int((self.persent) // self.size)+(1 if (int(self.persent % self.size)) == 0 else 0)) + (additional) + self.complete_symbol*(1 if (self._min_int(self.persent % self.size)) != 0 else 0)+ (additional)+self.uncomplete_symbol * self._min_int(((self.max_value - self.persent) / self.size)) + self.right_border +' ' + str(
                self.persent) + (f' of {self.max_value}' if self.show_of else '') + ' ' + self.units + (Fore.WHITE if self.colors else '') + (f' | {self._delta_time()} {self.units}/sec' if self.show_speed else '') +f' | {self.description}'

"""
An incredibly useful function.
"""
def base():
    import this

if __name__ == "__main__":
    import time
    load = Loader(description='Loading program', show_speed=True, size=801, max_value=100000, show_of=True, units='bytes')
    for _ in range(1, 100001):
        load.update(1)
        time.sleep(0.001)
        load.pr_load()