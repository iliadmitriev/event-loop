
class GenException(Exception):
    pass


def coroutine(func):
    def wrapper(*args, **kwargs):
        gen = func(*args, *kwargs)
        gen.send(None)
        return gen
    return wrapper


def sub_gen():
    while True:
        try:
            message = yield
        except StopIteration:
            break
        else:
            print('..........', message)

    return 'Sub_gen returned'


@coroutine
def delegator(g):
    # while True:
    #     try:
    #         data = yield
    #         g.send(data)
    #     except GenException as e:
    #         g.throw(e)
    result = yield from g
    print(result)


sg = sub_gen()
g = delegator(sg)
