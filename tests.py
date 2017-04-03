import unittest
from functions import *
import nltk

class TestSample(unittest.TestCase):

     def test_getNer_students_marks_courses(self):
         query1 = "anvesh marks tir"
         result1 = {'Student': ['Anvesh'], 'attributes': ['foo:marks'], 'Faculty': [], 'Course': ['Topics In Information Retrieval']}
         query2 = "How many marks did Anvesh and Nurendra get in Topics in IR and NLP?"
         result2 = {'Course': ['Natural Language Processing'], 'Faculty': [], 'Student': ['Nurendra', 'Anvesh'], 'attributes': ['foo:marks']}
         self.assertEqual(getNer(query1),result1)
         self.assertEqual(getNer(query2),result2)    


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSample)
    unittest.TextTestRunner(verbosity=2).run(suite)
