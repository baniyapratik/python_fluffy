from .timer import clock

class Logger:
    @clock
    def warning(self, *args):
        return args

    @clock
    def info(self, *args):
        return args