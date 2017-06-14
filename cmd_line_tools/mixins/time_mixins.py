import timeit


__all__ = ['TimingMixin']


class TimingMixin(object):
    def function_time(self, func):
        return timeit.timeit(func, number=100)