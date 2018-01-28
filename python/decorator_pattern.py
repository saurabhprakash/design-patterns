import abc

SMALL = 's'
LARGE = 'l'

class Pizza():
	__metaclass__ = abc.ABCMeta

	def __init__(self, size):
		self.size = size
		super().__init__()

	@abc.abstractmethod
	def cost(self):
		pass


class VegPizza(Pizza):

	def __init__(self, size):
		self.size = size

	def cost(self):
		if self.size == SMALL:
			return 100
		elif self.size == LARGE:
			return 200


class PizzaDecorator(Pizza):

	def __init__(self, pizza):
		self.pizza = pizza
		self.size = self.pizza.size

	def cost(self):
		return self.pizza.cost()


class CheezePizzaDecorator(PizzaDecorator):

	def __init__(self, pizza):
		super(CheezePizzaDecorator, self).__init__(pizza)

	def cost(self):
		return (20 if self.pizza.size == LARGE else 10)  + self.pizza.cost()


class CornPizzaDecorator(PizzaDecorator):

	def __init__(self, pizza):
		super(CornPizzaDecorator, self).__init__(pizza)

	def cost(self):
		return (25 if self.pizza.size == LARGE else 5)  + self.pizza.cost()
		return 25 + self.pizza.cost()

if __name__ == '__main__':
	
	vp1 = VegPizza(SMALL)
	cpd = CheezePizzaDecorator(vp1)
	print ("Cheeze Small Pizza cost=", cpd.cost())

	vp2 = VegPizza(LARGE)
	cpd2 = CornPizzaDecorator(vp2)
	print ("Corn Large Pizza cost=", cpd2.cost())
