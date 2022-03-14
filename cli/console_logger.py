def error(msg):
    """Wrapper for error messages"""
    return f"[red]{msg}[/red]"


def info(msg):
    """Wrapper for info messages"""
    return f"[blue]{msg}[/blue]"


def warning(msg):
    """Wrapper for warning messages"""
    return f"[yellow]{msg}[/yellow]"


console_functions = {
    'error': error,
    'warning': warning,
    'info': info
}
