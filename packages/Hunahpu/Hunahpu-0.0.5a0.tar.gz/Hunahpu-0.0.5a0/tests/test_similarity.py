import unittest
from hunahpu.Similarity import JCSimilarity, ColavSimilarity


class TestJC_similarity(unittest.TestCase):
    def setUp(self):
        self.title1 = "Implementation of industrial technology to improve the manufacturing "
        self.title1 += "process contoured seats [Implementación de la tecnología industrial "
        self.title1 += "para el mejoramiento del proceso de fabricación de asientos conformados]"
        self.title2 = "Implementation of industrial technology to improve the manufacturing process contoured seats"
        self.title3 = "Implementation of industrial technology to improve the manufacturing process contoured seats"

    def test__working(self):
        self.assertEqual(JCSimilarity(self.title2, self.title3), True)

    def test__failing(self):
        self.assertNotEqual(JCSimilarity(self.title1, self.title2), False)


class TestColav_similarity(unittest.TestCase):
    def setUp(self):
        self.title1 = "Implementation of industrial technology to improve the manufacturing "
        self.title1 += "process contoured seats [Implementación de la tecnología industrial "
        self.title1 += "para el mejoramiento del proceso de fabricación de asientos conformados]"
        self.title2 = "Implementation of industrial technology to improve the manufacturing process contoured seats"
        self.title3 = "Implementation of industrial technology to improve the manufacturing process contoured seats"
        self.paper1 = {'title': self.title1, 'journal': None, 'year': None}
        self.paper2 = {'title': self.title2, 'journal': None, 'year': None}
        self.paper3 = {'title': self.title3, 'journal': None, 'year': None}

    def test__working(self):
        self.assertEqual(ColavSimilarity(self.paper2, self.paper3), True)
        self.assertEqual(ColavSimilarity(
            self.paper2, self.paper3, use_translation=True), True)
        self.assertEqual(ColavSimilarity(
            self.paper2, self.paper3, use_parsing=False), True)

    def test__failing(self):
        self.assertEqual(ColavSimilarity(self.paper1, self.paper2), True)


if __name__ == '__main__':
    unittest.main()
