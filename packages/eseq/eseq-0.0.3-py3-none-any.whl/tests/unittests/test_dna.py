'''
Test class 
'''
from tests.helper import *
from src.eseq import DNA

@ddt
class TestDNA(TestCase):

    def test_(self):
        DNA('ATGC')

    @data(
        ['ATGC', 'TACG'],
        ['ATIN', 'TAIN'],
    )
    @unpack
    def test_complement(self, seq, expect):
        res = DNA(seq).complement()
        assert res == expect

    @data(
        ['ATGC', 'GCAT'],
    )
    @unpack
    def test_reverse_complement(self, seq, expect):
        res = DNA(seq).reverse_complement()
        assert res == expect

    # @data(
    #     ['ATGC', .5],
    #     ['GCGGC', 1],
    #     ['', 0],
    #     ['AB', 0],
    # )
    # @unpack
    # def test_calculate_gDNA(self, seq, expect):
    #     res = DNA(seq).calculate_gDNA()
    #     assert res == expect




    @data(
        ['ATGC', 'TGA', 2, [(1,3)]],
        ['ATGCTATGCT', 'TGCT', 4,  [(1, 4), (6, 9)]],
    )
    @unpack
    def test_detect_similarity(self, seq1, seq2, expect_max, expect):
        res = DNA(seq1).detect_similarity(seq2)
        assert res[0] == expect_max
        assert res[1] == expect

    @data(
        ['AAATAAA', 'AAATTT', 3],
        ['AAATAAA', 'TAAATTT', 0],
    )
    @unpack
    def test_detect_overlap(self, seq1, seq2, expect):
        res = DNA(seq1).detect_overlap(seq2)
        assert res == expect





