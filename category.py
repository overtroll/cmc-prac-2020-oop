class NotTradable(Exception):
    pass


class Item(object):
    def __init__(self, instrument):
        self.instrument_ = instrument
        self.position_ = 0

    def change_position(self, delta):
        if not self.instrument_.tradable():
            raise NotTradable('{} is not tradable'.format(self.instrument_.name()))

        self.position_ += delta

    def instrument(self):
        return self.instrument_

    def position(self):
        return self.position_

    def nav(self):
        return self.instrument_.price() * self.position_

    def __str__(self):
        tradable = ', Tradable' if self.instrument_.tradable() else ''
        return "{} x {}. {:.2f}$, Yield:{:.2f}%, Monthly default probability:{:.2f}%{}".format(
            self.position_,
            self.instrument_.name(),
            self.instrument_.price(),
            self.instrument_.expected_yield() * 100,
            self.instrument_.default_probability(),
            tradable)

    def month(self):
        cash, expired = self.instrument_.month()
        return cash * self.position_, expired


class Category(object):
    def __init__(self, name, factory, max_items=4):
        self.name_ = name
        self.factory_ = factory
        self.item_count_ = max_items
        self.items_ = []
        self.last_absolute_yield_ = None
        self.last_relative_yield_ = None
        self.generate()

    def find_instrument(self, instrument_name):
        for item in self.items_:
            if item.instrument().name() == instrument_name:
                return item

    def name(self):
        return self.name_

    def generate(self):
        for i in range(len(self.items_), self.item_count_):
            self.items_.append(Item(self.factory_()))

    def nav(self):
        result = 0
        for item in self.items_:
            result += item.nav()

        return result

    def __str__(self):
        if self.last_absolute_yield_ is None:
            gain = ''
        else:
            gain = 'Yield: {:.2f}$ = {:.2f}%.'.format(self.last_absolute_yield_, self.last_relative_yield_ * 100)

        result = '{}. NAV: {:.2f}$. {}\n'.format(self.name(), self.nav(), gain)
        for item in self.items_:
            result += (str(item) + '\n')

        return result

    def month(self):
        """
        :return: gained cash
        """
        prev_nav = self.nav()

        gained_cash = 0
        new_items = []
        for item in self.items_:
            cash, expired = item.month()
            gained_cash += cash
            if not expired and (item.position() > 0 or item.instrument().tradable()):
                new_items.append(item)

        self.items_ = new_items
        self.generate()

        if prev_nav < 1e-9:
            self.last_absolute_yield_ = 0
            self.last_relative_yield_ = 0
            return 0

        nav = self.nav() + gained_cash
        self.last_absolute_yield_ = nav - prev_nav
        self.last_relative_yield_ = (nav - prev_nav) / prev_nav
        return gained_cash
