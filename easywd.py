import random
import collections
import functools
import os

languages = {}


class Memoized(object):
    """Decorator. Caches a function"s return value each time it is called.
    If called later with the same arguments, the cached value is returned
    (not reevaluated).
    """

    def __init__(self, func):
        self.func = func
        self.cache = {}

    def __call__(self, *args):
        if not isinstance(args, collections.Hashable):
            # uncacheable. a list, for instance.
            # better to not cache than blow up.
            return self.func(*args)
        if args in self.cache:
            return self.cache[args]
        else:
            value = self.func(*args)
            self.cache[args] = value
            return value

    def __repr__(self):
        """Return the function"s docstring."""
        return self.func.__doc__

    def __get__(self, obj, objtype):
        """Support instance methods."""
        return functools.partial(self.__call__, obj)


def make_password(language, pwd_size, sep):
    words_by_size = languages[language]
    combinations = find_combinations(pwd_size, language, len(sep))
    choice = weighted_choice(combinations)
    pwd = ""
    for size in choice:
        word = random.choice(words_by_size[size])
        if random.randint(0, 1):
            word = word.upper()
        if pwd:
            pwd += sep + word
        else:
            pwd += word
    return pwd


def weighted_choice(choices):
    total = sum(w for c, w in choices)
    r = random.uniform(0, total)
    upto = 0
    for c, w in choices:
        if upto + w >= r:
            return c
        upto += w
    assert False, "No choices available"


@Memoized
def find_combinations(pwd_size, language, sep_len):
    result = find_combinations_rec(pwd_size, language, sep_len)
    print "found:", len(result), "combinations"
    return result


def find_combinations_rec(pwd_size, language, sep_len, combinations=[], partial=()):
    words_by_size = languages[language]
    word_sizes = words_by_size.keys()
    if partial:
        partial_length = sum(partial) + sep_len * (len(partial) - 1)
    else:
        partial_length = 0
        combinations = []
    if partial_length == pwd_size:
        chances = 1
        for size in partial:
            chances *= len(words_by_size[size])
        combinations.append((partial, chances))
        return  # found one
    if partial_length > pwd_size:
        return  # if we reach the number why bother to continue
    possible_sizes = [s for s in word_sizes if s + partial_length <= pwd_size]
    for i in range(len(possible_sizes)):
        size = word_sizes[i]
        find_combinations_rec(pwd_size, language, sep_len, combinations, partial + (size,))
    return combinations


# load word file into a dict where:
#   key: length
#   val: tuple of words of that length
def load_words(language):
    word_lengths = {}
    path = os.path.dirname(os.path.realpath(__file__)) + os.sep
    with open("{}dict-{}.txt".format(path, language)) as f:
        lines = f.readlines()
    results = {}
    for line in lines:
        word = line.strip()
        wlen = len(word)
        word_lengths[word] = wlen
        try:
            results[wlen]
        except KeyError:
            results[wlen] = ()
        results[wlen] += (word,)
    return results


for lang in ["en", "es"]:
    languages[lang] = load_words(lang)
    print "loaded", lang, "dictionary"
