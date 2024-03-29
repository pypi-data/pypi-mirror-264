from functools import partial

problems = {}

# a decorator to store functions in problems as we go
def add_to_problems(shortname, function):
    """
    add a problem to the problems dict
    """
    name = function.__name__.replace("_", "-")
    def wrapped():
        raw = function()
        raw['shortname'] = shortname
        return raw
    problems[name] = wrapped
    return wrapped


@partial(add_to_problems, "short")
def knuth_original():
    return dict(value="Bingo")

print(problems['knuth-original']())
