from unittest import TestCase
import generate


class GenerateTest(TestCase):
	def test_invalid_usage(self):
		self.assertEqual(2, generate._main(["foo"]))
		for command in ["detail", "overview", "areas", "all"]:
			self.assertEqual(3, generate._main([command]))

		for command in ["detail", "overview", "areas", "all"]:
			self.assertEqual(5, generate._main([command, "1234"]))

		self.assertEqual(4, generate._main(["area"]))
		self.assertEqual(4, generate._main(["area", "foo"]))