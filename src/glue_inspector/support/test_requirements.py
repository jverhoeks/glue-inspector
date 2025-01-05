import unittest

from glue_inspector.support.requirements import Requirement, Requirements


class RequirementTests(unittest.TestCase):
    def test_parse_valid_line(self):
        line = "requests==2.25.1"
        req = Requirement(line)
        self.assertEqual(req.name, "requests")
        self.assertEqual(req.operator, "==")
        self.assertEqual(req.version, "2.25.1")

    def test_parse_invalid_line(self):
        line = "invalid_line"
        req = Requirement(line)
        self.assertEqual(req.name, None)
        self.assertEqual(req.operator, None)
        self.assertEqual(req.version, None)

    def test_str_representation(self):
        line = "requests==2.25.1"
        req = Requirement(line)
        self.assertEqual(str(req), "requests==2.25.1")


class RequirementsTests(unittest.TestCase):
    def setUp(self):
        self.requirements = Requirements()

    def test_as_str(self):
        req1 = Requirement("requests==2.25.1")
        req2 = Requirement("numpy>=1.19.0")
        self.requirements.add(req1)
        self.requirements.add(req2)
        expected_str = "requests==2.25.1\nnumpy>=1.19.0"
        self.assertEqual(self.requirements.as_str(), expected_str)

    def test_as_list(self):
        req1 = Requirement("requests==2.25.1")
        req2 = Requirement("numpy>=1.19.0")
        self.requirements.add(req1)
        self.requirements.add(req2)
        expected_list = ["requests==2.25.1", "numpy>=1.19.0"]
        self.assertEqual(self.requirements.as_list(), expected_list)

    def test_write(self):
        file = "test_requirements.txt"
        req1 = Requirement("requests==2.25.1")
        req2 = Requirement("numpy>=1.19.0")
        self.requirements.add(req1)
        self.requirements.add(req2)
        self.requirements.write(file)
        with open(file, "r") as f:
            content = f.read()
        expected_content = "requests==2.25.1\nnumpy>=1.19.0"
        self.assertEqual(content, expected_content)

    def test_read(self):
        file = "test_requirements.txt"
        content = "requests==2.25.1\nnumpy>=1.19.0"
        with open(file, "w") as f:
            content = f.write(content)

        self.requirements.read(file)
        self.assertEqual(len(self.requirements.data), 2)
        self.assertIn("requests", self.requirements.data)
        self.assertIn("numpy", self.requirements.data)

    def test_add(self):
        req = Requirement("requests==2.25.1")
        self.requirements.add(req)
        self.assertIn("requests", self.requirements.data)
        self.assertEqual(self.requirements.data["requests"], req)

    def test_add_line(self):
        line = "requests==2.25.1"
        self.requirements.add_line(line)
        self.assertIn("requests", self.requirements.data)
        self.assertEqual(self.requirements.data["requests"].name, "requests")
        self.assertEqual(self.requirements.data["requests"].operator, "==")
        self.assertEqual(self.requirements.data["requests"].version, "2.25.1")

    def test_add_line_with_existing_requirement(self):
        line = "requests==2.25.1"
        self.requirements.add_line(line)
        self.assertIn("requests", self.requirements.data)
        self.assertEqual(self.requirements.data["requests"].name, "requests")
        self.assertEqual(self.requirements.data["requests"].operator, "==")
        self.assertEqual(self.requirements.data["requests"].version, "2.25.1")

        line = "requests>=2.26.0"
        self.requirements.add_line(line)
        self.assertIn("requests", self.requirements.data)
        self.assertEqual(self.requirements.data["requests"].name, "requests")
        self.assertEqual(self.requirements.data["requests"].operator, ">=")
        self.assertEqual(self.requirements.data["requests"].version, "2.26.0")

    def testmerge(self):
        line = "requests==2.25.1"
        self.requirements.add_line(line)

        reqs = Requirements()
        line2 = "requests==2.25.2"
        reqs.add_line(line2)
        self.requirements.merge(reqs)

        self.assertIn("requests", self.requirements.data)
        self.assertEqual(self.requirements.data["requests"].name, "requests")
        self.assertEqual(self.requirements.data["requests"].operator, "==")
        self.assertEqual(self.requirements.data["requests"].version, "2.25.2")


if __name__ == "__main__":
    unittest.main()
