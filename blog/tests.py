from django.test import TestCase

# Create your tests here.
# def test_sum():
# 	assert sum([1, 2, 3]) == 6, "Хорошо бы sex"
#
# def test_sum_2():
# 	assert sum((1, 2, 4)) == 6, "Хорошо бы всех sex"
#
# if __name__ == "__main__":
# 	test_sum()
# 	test_sum_2()
# 	print("Все хорошо")


import unittest

class TestSum(unittest.TestCase):
	def test_sum(self):
		self.assertEqual(sum([1, 2, 3]) == 6, "Хорошо бы sex")

	def test_sum_2(self):
		self.assertEqual(sum((1, 2, 3)) == 6, "Хорошо бы всех sex")

if __name__ == "__main__":
	unittest.main()