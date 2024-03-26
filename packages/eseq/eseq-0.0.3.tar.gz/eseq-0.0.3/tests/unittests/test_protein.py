'''
Test class 
'''
from unittest import TestCase, mock
from ddt import ddt, data, unpack
import os, sys
from src.eseq import Protein

@ddt
class Test_(TestCase):

    def setUp(self):
        pass
    
    @data(
        # N-glycosylation site
        ['', 'N-{P}-[ST]-{P}', 4, []],
    )
    @unpack
    def test_detect_motif(self, seq, prosite, k, expect):
        pass
        