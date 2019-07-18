import unittest
from Core import validate_fifteen

class CoreTest(unittest.TestCase):
		
	def test_validate_fifteen(self):
		first_list = [1,5,9]
		second_list = [3,5,7]
		third_list = [4,5,6]
		forth_list = [3,6,9] #should fail for this one
		
		self.assertEqual(validate_fifteen(first_list,15), True)
		self.assertEqual(validate_fifteen(second_list,15), True)
		self.assertEqual(validate_fifteen(third_list,15), True)
		self.assertEqual(validate_fifteen(first_list,15), False)
		
	def test_a_win(self):
		list1 = [1,5,8,9]
		list2 = [2,4,5,8]
		list3 = [3,5,6,7]
	
if __name__ == '__main__':
	unittest.main()

