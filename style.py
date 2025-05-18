from colorama import init, Fore, Style

def showStyledTitleCyan(message):
    init()
    border = "═" * (len(message) + 4)
    top = f"╔{border}╗"
    bottom = f"╚{border}╝"
    middle = f"║  {message}  ║"

    print(Fore.MAGENTA + Style.BRIGHT + top)
    print(middle)
    print(bottom + Style.RESET_ALL)

def showStyledTitleGreen(message):
    init()
    border = "═" * (len(message) + 4)
    top = f"╔{border}╗"
    bottom = f"╚{border}╝"
    middle = f"║  {message}  ║"

    print(Fore.GREEN + Style.BRIGHT + top)
    print(middle)
    print(bottom + Style.RESET_ALL)

def showStyledTitleYellow(message):
    init()
    border = "═" * (len(message) + 4)
    top = f"╔{border}╗"
    bottom = f"╚{border}╝"
    middle = f"║  {message}  ║"

    print(Fore.YELLOW + Style.BRIGHT + top)
    print(middle)
    print(bottom + Style.RESET_ALL)

def showStyledTitleReset(message):
    init()
    border = "═" * (len(message) + 4)
    top = f"╔{border}╗"
    bottom = f"╚{border}╝"
    middle = f"║  {message}  ║"

    print(Fore.RESET + Style.BRIGHT + top)
    print(middle)
    print(bottom + Style.RESET_ALL)