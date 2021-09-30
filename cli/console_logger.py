from rich import print

def error(msg):
    print(f"[red]{msg}[/red]")

def info(msg):
    print(f"[blue]{msg}[/blue]")

def warning(msg):
    print(f"[yellow]{msg}[/yellow]")

console_functions = {
    'error': error,
    'warning': warning,
    'info': info
}