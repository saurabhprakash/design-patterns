"""
    Observer pattern in python implementation
    Newspaper being main subject 
    and Users/Readers being their observers(subscribers)
"""

import abc

class Observer(object):
    """observers(subscribers) abstract base class
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def get_news(self, news):
        """get news abstract method"""
        return

class NewspaperABC(object):
    """Newspaper abstract base class
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def register_observer(self, observer):
        """add a subscriber"""
        return

    @abc.abstractmethod
    def notify_observer(self):
        """notify all subscriber"""
        return

    @abc.abstractmethod
    def remove_observer(self, observer):
        """remove a subscriber"""
        return

class News(NewspaperABC):

    def __init__(self):
        self.observers = []
        self.news = ''

    def register_observer(self, observer):
        """add a subscriber"""
        self.observers.append(observer)

    def remove_observer(self, observer):
        """remove a subscriber"""
        self.observers.remove(observer)

    def notify_observer(self):
        """notify all subscriber"""
        for observer in self.observers:
            observer.get_news(self.news)
        
    def add_news(self, news):
        """adds a news to system"""
        self.news = news
        self.notify_observer()

class Reader(Observer):
    """class Reader child of Observer"""

    def __init__(self, name):
        self.reader_name = name

    def get_news(self, news):
        """get news implementation"""
        print("%s read news: %s" % (self.reader_name, news))

if __name__ == '__main__':
    n = News()

    r1 = Reader('Arya')
    n.register_observer(r1)

    r2 = Reader('Sansa')
    n.register_observer(r2)

    n.add_news("Game Of Thrones fans have an incredible theory about what the Night King's plans really are")
    n.add_news("Jeff Bezos is demanding Amazon make him a Game Of Thrones")
    
