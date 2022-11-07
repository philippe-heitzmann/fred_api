import time 

def timeit(func):
    def inner(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        print(f'{round(time.time() - start_time, 1)}s to complete')
        return result
    return inner 