from traceback import print_stack


def error_handling(func):
    """Provide a general purpose function wrapper for error handling"""
    def inner_func(*args, **kwargs):
        """Inner funtion returned when calling"""
        try:
            func(*args, **kwargs)
        except Exception as e:
            print_stack(e)
    return inner_func
