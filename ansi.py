
class ansi:
    """
    This class contains the ANSI escape codes for printing to the console as
    well as commonly used combinations of these codes.
    """

    reset = "\033[0m"
    bold = "\033[1m"
    faint = "\033[2m"
    italic = "\033[3m"
    underline = "\033[4m"
    blink = "\033[5m"
    inverse = "\033[7m"

    class fg:
        black = "\033[30m"
        red = "\033[31m"
        green = "\033[32m"
        yellow = "\033[33m"
        blue = "\033[34m"
        magenta = "\033[35m"
        cyan = "\033[36m"
        white = "\033[37m"

        grey = "\033[90m"
        bright_red = "\033[91m"
        bright_green = "\033[92m"
        bright_yellow = "\033[93m"
        bright_blue = "\033[94m"
        bright_magenta = "\033[95m"
        bright_cyan = "\033[96m"
        bright_white = "\033[97m"

    class bg:
        black = "\033[40m"
        red = "\033[41m"
        green = "\033[42m"
        yellow = "\033[43m"
        blue = "\033[44m"
        magenta = "\033[45m"
        cyan = "\033[46m"
        white = "\033[47m"

        grey = "\033[100m"
        bright_red = "\033[101m"
        bright_green = "\033[102m"
        bright_yellow = "\033[103m"
        bright_blue = "\033[104m"
        bright_magenta = "\033[105m"
        bright_cyan = "\033[106m"
        bright_white = "\033[107m"

    @classmethod
    def ok(cls, content):
        return cls.fg.bright_green + cls.bold + str(content) + cls.reset

    @classmethod
    def error(cls, content):
        return cls.fg.bright_red + cls.bold + str(content) + cls.reset

    @classmethod
    def warning(cls, content):
        return cls.fg.bright_yellow + cls.bold + str(content) + cls.reset

    @classmethod
    def printok(cls, content, flush=False, end='\n'):
        print(cls.ok(content), flush=flush, end=end)

    @classmethod
    def printerror(cls, content, flush=False, end='\n'):
        print(cls.error(content), flush=flush, end=end)

    @classmethod
    def printwarning(cls, content, flush=False, end='\n'):
        print(cls.warning(content), flush=flush, end=end)
