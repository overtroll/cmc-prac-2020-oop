from instrument import Instrument
from utils import rand_range_f, is_default
from name_generator import generate_name
from monthly_result import MonthlyResult, default, unchanged
import random


class Bond(Instrument):
    def __init__(self, name, price, monthly_yield, default_probability,
                 months_to_maturity):
        self.name_ = name
        self.price_ = price
        self.monthly_yield_ = monthly_yield
        self.months_to_maturity_ = months_to_maturity
        self.months_elapsed_ = 0
        self.default_probability_ = default_probability

    def tradable(self):
        return self.months_elapsed_ == 0

    def name(self):
        return self.name_

    def price(self):
        return self.price_

    def expected_yield(self):
        return self.monthly_yield_

    def default_probability(self):
        return self.default_probability_

    def month(self):
        if is_default(self.default_probability_):
            return default

        self.months_elapsed_ += 1
        current_yield = self.price_ * self.monthly_yield_

        if self.months_elapsed_ == self.months_to_maturity_:
            return MonthlyResult(self.price_ + current_yield, True)

        return MonthlyResult(current_yield, False)

    @staticmethod
    def factory(min_price=10.0, max_price=200.0, max_monthly_yield=0.06, min_default_probability=0,
                max_default_probability=0.001, min_months_to_maturity=1,
                max_months_to_maturity=12):
        def generate():
            name = generate_name("xxxxx")
            price = rand_range_f(min_price, max_price)
            monthly_yield = rand_range_f(0, max_monthly_yield)
            default_probability = rand_range_f(min_default_probability, max_default_probability)
            months_to_maturity = random.randint(min_months_to_maturity, max_months_to_maturity)
            return Bond(name, price, monthly_yield, default_probability,
                        months_to_maturity)

        return generate
