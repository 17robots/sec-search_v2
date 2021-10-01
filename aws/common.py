from traceback import print_stack


def error_handling(func):
    def inner_func(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            print_stack(e)
    return inner_func
