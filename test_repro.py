import unittest

class MyTestCase(unittest.TestCase):
    def setUp(self):
        raise NameError("xxx in setUp")
    @unittest.skip("hello")
    def test_one(self):
        pass
    def tearDown(self):
        raise NameError("xxx in tearDown")