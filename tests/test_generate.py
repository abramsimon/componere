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

	def test_areas_parsing(self):
		areas = generate._load_areas("test_areas.yaml")
		self.assertEqual(3, len(areas))

		empty = areas["partial"]
		self.assertNotEqual(None, empty)
		self.assertEqual(u"Partial", empty.name)
		self.assertEqual(None, empty.parent_identifier)

		all = areas["all"]
		self.assertNotEqual(None, all)
		self.assertEqual(u"All", all.name)
		self.assertEqual("partial", all.parent_identifier)


	def test_levels_parsing(self):
		levels = generate._load_levels("test_levels.yaml")
		self.assertEqual(2, len(levels))

		level10 = levels["level-10"]
		self.assertNotEqual(None, level10)
		self.assertEqual(u"Level 10", level10.name)
		self.assertEqual(10, level10.order)
