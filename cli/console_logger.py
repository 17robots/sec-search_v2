def error(msg):
    """wrapper for error messages"""
    return f"[red]{msg}[/red]"


def info(msg):
    """wrapper for info messages"""
    return f"[blue]{msg}[/blue]"


def warning(msg):
    """wrapper for warning messages"""
    return f"[yellow]{msg}[/yellow]"


console_functions = {
    'error': error,
    'warning': warning,
    'info': info
}
