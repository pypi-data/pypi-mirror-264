'''
Test class 
'''
from tests.helper import *
from src.eseq import Compress

@ddt
class TestCompress(TestCase):

    @data(
        ['AATTTGCCC',[('A', 2), ('T', 3), ('G', 1), ('C', 3)]],
        ['ATGC', [('A', 1), ('T', 1), ('G', 1), ('C', 1)]],
        ['A', [('A', 1)]],
        ['ACCCCCCC', [('A', 1), ('C', 7)]],
        ['TTTT', [('T',4)]],
        ['', []],
    )
    @unpack
    def test_encode_repeat(self, input, expect):
        res = Compress.encode_repeat(input)
        assert res == expect


    @data(
        ['AATTTGCCC','A2T3GC3'],
        ['ATGC', 'ATGC'],
        ['A', 'A'],
        ['ACCCCCCC', 'AC7'],
        ['TTTT', 'T4'],
        ['', ''],
    )
    @unpack
    def test_to_encoded_seq(self, input, expect):
        res = Compress.to_encoded_seq(input)
        assert res == expect



    @data(
        ['A2T3GC3', 'AATTTGCCC'],
        ['ATGC', 'ATGC'],
        ['AC7', 'ACCCCCCC'],
    )
    @unpack
    def test_decode_repeat(self, input, expect):
        res = Compress.decode_repeat(input)
        assert res == expect
