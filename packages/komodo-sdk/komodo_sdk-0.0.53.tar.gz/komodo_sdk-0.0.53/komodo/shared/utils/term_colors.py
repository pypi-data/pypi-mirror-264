class TerminalColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_colored(message, color):
    print(color, sep='', end='')
    print(message)
    print(TerminalColors.ENDC, sep='', end='')


def print_warning(message):
    print_colored(message, TerminalColors.WARNING)


def print_error(message):
    print_colored(message, TerminalColors.FAIL)


def print_success(message):
    print_colored(message, TerminalColors.OKGREEN)


def print_info(message):
    print_colored(message, TerminalColors.OKBLUE)


def print_cyan(message):
    print_colored(message, TerminalColors.OKCYAN)


def print_header(message):
    print_colored(message, TerminalColors.HEADER)


def print_bold(message):
    print_colored(message, TerminalColors.BOLD)


if __name__ == '__main__':
    print_warning("This is a warning message")
    print_error("This is an error message")
    print_success("This is a success message")
    print_info("This is an info message")
    print_header("This is a header message")
    print_bold("This is a bold message")
    print_blue("This is a blue message")
    print_blue({'foo', 'bar'})
    print_blue(['foo', 'bar'])
