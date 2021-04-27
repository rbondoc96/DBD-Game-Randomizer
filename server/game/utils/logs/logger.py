from colorama import (
    Fore, Style, 
    init as colorama_init, 
    deinit as colorama_deinit
)

"""Logger class
Lets user log with 4 log levels.

In the order of least or highest severity:

0. DEBUG
1. INFO
2. WARN
3. ERROR
"""
class Logger:
    def __init__(self, tag):
        self.tag = tag
        colorama_init()

    def __del__(self):
        colorama_deinit()
        
    def _get_preamble(self, log_level):
        level = log_level.lower()
        
        # Default for "info" and unspecified log levels
        color = Fore.RESET

        if level == "debug":
            color = Fore.LIGHTBLUE_EX
        elif level == "warn":
            color = Fore.LIGHTYELLOW_EX
        elif level == "error":
            color = Fore.LIGHTRED_EX
        
        return (color, f"[{self.tag}]",)

    def _console_print(self, args):
        buff = (Style.RESET_ALL,)
        buff = args + buff

        for s in buff:
            print(s, end=" ")
        print("\n", end="")
            

    def log(self, *args):
        self._console_print(args)


    def debug(self, *args):
        color = self._get_preamble("debug")
        args = color + args
        self._console_print(args)        


    def info(self, *args):
        color = self._get_preamble("info")
        args = color + args
        self._console_print(args)


    def warn(self, *args):
        color = self._get_preamble("warn")
        args = color + args
        self._console_print(args)        


    def error(self, *args):
        preamble = self._get_preamble("error")
        args = color + args
        self._console_print(args)
