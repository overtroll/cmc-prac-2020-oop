import abc


class Instrument(abc.ABC):
    @abc.abstractmethod
    def name(self):
        pass

    @abc.abstractmethod
    def price(self):
        pass

    @abc.abstractmethod
    def tradable(self):
        pass

    @abc.abstractmethod
    def month(self):
        """
        :return: The amount of cash per month
        """
        pass

    @abc.abstractmethod
    def expected_yield(self):
        pass

    @abc.abstractmethod
    def default_probability(self):
        pass
