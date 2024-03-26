'''
Test class 
'''
from tests.helper import *
from src.eseq import RNA

@ddt
class Test_(TestCase):

    def setUp(self):
        pass

    def test_(self):
        pass
    
    def test_to_dna(self):
        res = RNA('GAUCUA').back_transcribe()
        assert res == 'GATCTA'