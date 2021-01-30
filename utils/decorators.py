import time 

# TODO: Come up with a better name!
def timeit(func):
    def wrapper(*args, **kwargs):
        t1 = time.time()
        func(*args, **kwargs)
        t = time.time() - t1
        print('Execution time: {} sec'.format(t))
        return func(*args, **kwargs)

    return wrapper