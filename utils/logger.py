from .timer import clock

class Logger:
    '''
    This class is for logging mechanism
    '''
    @clock
    def warning(self, *args):
        return args

    @clock
    def info(self, *args):
        return args