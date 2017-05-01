import unittest
from functions import *
import nltk

class TestSample(unittest.TestCase):

	def test_getNer_students_marks_courses(self):
		query_result1 = getNer("anvesh marks tir")
		result1 = {'Student': ['Anvesh'], 'attributes': ['foo:marks'], 'Faculty': [], 'Course': ['Topics In Information Retrieval']}
		query_result2 = getNer("How many marks did Anvesh and Nurendra get in Topics in IR and NLP?")
		result2 = {'Course': ['Natural Language Processing'], 'Faculty': [], 'Student': ['Nurendra', 'Anvesh'], 'attributes': ['foo:marks']}
		self.assertEqual(sorted(query_result1['Student']),sorted(result1['Student']))
		self.assertEqual(sorted(query_result2['Student']),sorted(result2['Student']))
		self.assertEqual(sorted(query_result1['attributes']),sorted(result1['attributes']))
		self.assertEqual(sorted(query_result2['attributes']),sorted(result2['attributes']))
		self.assertEqual(sorted(query_result1['Course']),sorted(result1['Course']))
		self.assertEqual(sorted(query_result2['Course']),sorted(result2['Course']))
		self.assertEqual(sorted(query_result1['Faculty']),sorted(result1['Faculty']))
		self.assertEqual(sorted(query_result2['Faculty']),sorted(result2['Faculty']))

	def test_get_faculty(self):
		query_ner1=getNer("anvesh marks tir")
		query_result1=getFaculty(query_ner1)
		result1="Faculty of Topics In Information Retrieval: Manish Shrivastava"
		query_ner2=getNer("How many marks did Anvesh and Nurendra get in Topics in IR and NLP?")
		query_result2=getFaculty(query_ner2)
		result2="Faculty of Natural Language Processing: Manish Shrivastava"
		self.assertEqual(query_result1,result1)
		self.assertEqual(query_result2,result2)

	def test_getEmailofStudent(self):
		query_ner1=getNer("what is anvesh's email id?") 
		query_result1 = getEmail_Student(query_ner1)
		result1=["Email of Anvesh : vijjinianvesh.rao@research.iiit.ac.in"]
		query_ner2=getNer("Nurendra's and Anvesh's email id")
		query_result2=getEmail_Student(query_ner2)
		result2=['Email of Nurendra : nurendra.choudhary@research.iiit.ac.in', \
		'Email of Anvesh : vijjinianvesh.rao@research.iiit.ac.in']
		self.assertEqual(sorted(query_result1),sorted(result1))
		self.assertEqual(sorted(query_result2),sorted(result2))


if __name__ == '__main__':
	suite = unittest.TestLoader().loadTestsFromTestCase(TestSample)
	unittest.TextTestRunner(verbosity=2).run(suite)
