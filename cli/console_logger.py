from rich import print


def error(msg):
    return f"[red]{msg}[/red]"


def info(msg):
    return f"[blue]{msg}[/blue]"


def warning(msg):
    return f"[yellow]{msg}[/yellow]"


console_functions = {
    'error': error,
    'warning': warning,
    'info': info
}
