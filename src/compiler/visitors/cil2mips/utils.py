def flatten(iterable):
    for item in iterable:
        try:
            yield from flatten(item)
        except TypeError:
            yield item
