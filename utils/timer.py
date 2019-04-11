import time

def clock(func):
    '''
    This wrapper used for getting the time taken by a funcition
    '''
    def clocked(*args):
        t0 = time.perf_counter()
        result = func(*args)
        elapsed = time.perf_counter() - t0
        name = func.__name__
        arg_str = ','.join(repr(arg) for arg in args)
        print('[%0.8fs] %s(%s) --> %r' % (elapsed, name, arg_str, result))
        return result
    return clocked