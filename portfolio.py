TAX_RATE = 0.17


class InsufficentMoney(Exception):
    pass


class InsufficientPosition(Exception):
    pass


class InstrumentNotFound(Exception):
    pass


class Portfolio(object):
    def __init__(self, categories):
        self.categories_ = categories
        self.last_absolute_yield_ = None
        self.last_relative_yield_ = None
        self.cash_ = 0
        self.elasped_months_ = 0

    def categories(self):
        return self.categories_

    def nav(self):
        result = self.cash_
        for item in self.categories_:
            result += item.nav()

        return result

    def header(self):
        if self.last_absolute_yield_ is None:
            gain = ''
        else:
            gain = 'Yield: {:.2f}$ = {:.2f}%.'.format(self.last_absolute_yield_, self.last_relative_yield_ * 100)

        result = 'NAV: {:.2f}$. Cash: {:.2f}$. {}\n--------\n'.format(
            self.nav(), self.cash_, gain)

        return result

    def month(self, on_info):
        prev_nav = self.nav()
        self.elasped_months_ += 1

        for category in self.categories_:
            self.cash_ += category.month()

        if prev_nav < 1e-9:
            self.last_absolute_yield_ = 0
            self.last_relative_yield_ = 0
            return

        profit = self.nav() - prev_nav

        self.cash_ -= profit * TAX_RATE
        if self.cash_ < 0:
            on_info("The government has given you {:.2f}$ tax relief".format(-self.cash_))
            self.cash_ = 0

        self.last_absolute_yield_ = self.nav() - prev_nav
        self.last_relative_yield_ = self.last_absolute_yield_ / prev_nav

    def find_instrument(self, instrument_name):
        for category in self.categories_:
            item = category.find_instrument(instrument_name)
            if item is not None:
                return item

        raise InstrumentNotFound("Instrument not found: " + str(instrument_name))

    def buy(self, amount, instrument_name):
        amount = float(amount)

        item = self.find_instrument(instrument_name)
        cash = item.instrument().price() * amount
        if cash > self.cash_:
            raise InsufficentMoney(
                "Requires {:.2f}$ cash while only have {:.2f}$ ".format(
                    cash, self.cash_
                ))

        self.cash_ -= cash
        item.change_position(amount)

    def sell(self, amount, instrument_name):
        amount = float(amount)

        item = self.find_instrument(instrument_name)
        if item.position() < amount:
            raise InsufficientPosition(
                "Position of at least {:.2f} required, got only {:.2f}".format(
                    amount, item.position()))

        item.change_position(-amount)
        self.cash_ += amount * item.instrument().price()

    def add_cash(self, amount):
        amount = float(amount)

        self.cash_ += amount

    def remove_cash(self, amount):
        amount = float(amount)

        if amount > self.cash_:
            raise InsufficentMoney(
                "Requires {:.2f}$ cash while only have {:.2f}$ ".format(
                    amount, self.cash_
                ))
