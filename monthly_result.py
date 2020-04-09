import collections

MonthlyResult = collections.namedtuple('MonthlyResult', ['cash', 'expired'])

default = MonthlyResult(cash=0, expired=True)

unchanged = MonthlyResult(cash=0, expired=False)