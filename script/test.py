
class Test(object):
	def __init__(self):
		self.name = 'hahahahha'
		name1 = '2233'
		_name2 = '666'
		__name3 = '777'
	def print_name(self):
		print(self.name)

a1 = Test()
print(a1.name)
a1.print_name()
# print(a1._Test__name2)
# print(Test._Test__name3)
# print(Test.__dict__)