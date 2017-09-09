from abc import ABCMeta, abstractmethod

class Base(metaclass=ABCMeta):

    def method1(self):
        """this method is not compulsory to define in child class"""
        pass

    @abstractmethod
    def method2(self):
        """this method is compulsory to define in child class"""
        pass


class Child(Base):

    def method1(self):
        print ('i am method 1')

    def method2(self):
        print ('i am method 2') 

if __name__ == '__main__':
    child = Child()
    child.method1()
    child.method2()