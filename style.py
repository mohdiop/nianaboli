from colorama import init, Fore, Style

def showStyledTitle(message):
    init()
    border = "═" * (len(message) + 4)
    top = f"╔{border}╗"
    bottom = f"╚{border}╝"
    middle = f"║  {message}  ║"

    print(Fore.CYAN + Style.BRIGHT + top)
    print(middle)
    print(bottom + Style.RESET_ALL)