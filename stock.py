from instrument import Instrument
from utils import rand_range_f, is_default
from name_generator import generate_name
from monthly_result import default, unchanged


class Stock(Instrument):
    def __init__(self, name, price, expected_yield, bankrupcy_probability, volatility):
        self.name_ = name
        self.price_ = price
        self.expected_yield_ = expected_yield
        self.default_probability_ = bankrupcy_probability
        self.volatility_ = volatility

    def tradable(self):
        return True

    def name(self):
        return self.name_

    def price(self):
        return self.price_

    def expected_yield(self):
        return self.expected_yield_

    def default_probability(self):
        return self.default_probability_

    def month(self):
        if is_default(self.default_probability_):
            return default

        current_yield = self.expected_yield_ + rand_range_f(-self.volatility_, self.volatility_)
        self.price_ *= (1.0 + current_yield)
        return unchanged

    @staticmethod
    def factory(*, min_price=1000.0, max_price=3000.0, max_monthly_yield=0.1, min_default_probability=0,
                max_default_probability=0.4, min_volatility=0, max_volatility=0.2):
        def generate():
            name = generate_name("XXXX")
            price = rand_range_f(min_price, max_price)
            monthly_yield = rand_range_f(0, max_monthly_yield)
            default_probability = rand_range_f(min_default_probability, max_default_probability)
            volatility = rand_range_f(min_volatility, max_volatility)
            return Stock(name, price, monthly_yield, default_probability, volatility)

        return generate
