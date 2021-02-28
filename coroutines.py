
def coroutine(func):
    def wrapper(*args, **kwargs):
        gen = func(*args, *kwargs)
        gen.send(None)
        return gen
    return wrapper


@coroutine
def average():
    count = 0
    total = 0
    avg = None

    while True:
        try:
            x = yield avg
        except StopIteration:
            print('Done')
        else:
            count += 1
            total += x
            avg = round(total / count, 2)


av_gen = average()
print(av_gen.send(400))
print(av_gen.send(200))
av_gen.throw(StopIteration)
