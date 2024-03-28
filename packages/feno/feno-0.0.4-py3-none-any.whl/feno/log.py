class Log:
    verbose = False
    
    @staticmethod
    def debug(*args, **kwargs):
        if Log.verbose:
            print(*args, **kwargs)

    @staticmethod
    def write(*args, **kwargs):
        if Log.verbose:
            print(*args, **kwargs)
        else:
            print(*args, **kwargs, end="", flush=True)
