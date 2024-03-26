'''
Test class 
'''
from tests.helper import *
from src.eseq import Seq

@ddt
class TestSeq(TestCase):

    @data(
        ['ATGC', 'ATGC'],
        ['AT\nGC', 'ATGC'],
        ['AtgC', 'ATGC'],
        ['', ''],
    )
    @unpack
    def test_(self, seq, expect):
        res = Seq(seq)
        assert getattr(res, 'seq') == expect

    @data(
        ['ATGC', 4],
        ['', 0],
    )
    @unpack
    def test_length(self, seq, expect):
        res = Seq(seq).length()
        assert res == expect

    @data(
        ['ATGC', 'CGTA'],
        ['', ''],
    )
    @unpack
    def test_reverse(self, seq, expect):
        res = Seq(seq).reverse()
        assert res == expect

    @data(
        ['ATGCCGCT', 'GC', 2],
        ['ATGCCGCT', 'C', 3],
        ['ATGCCGCT', 'GT', 0],
        ['ATGCCGCT', '', 0],
        ['ATGCCGCT', 'ATGCCGCT', 1],
    )
    @unpack
    def test_count_sub_seq(self, seq, sub_seq, expect):
        res = Seq(seq).count_sub_seq(sub_seq)
        assert res == expect

    @data(
        ['AAC', {'C':1, 'A':2}],
        ['', {}],
    )
    @unpack
    def test_count_occurrence(self, seq, expect):
        res = Seq(seq).count_occurrence()
        assert res == expect

    @data(
        ['ATGCCGCT', 'GC', [(2,4),(5,7)],],
        ['ATGCCGCT', 'AGC', [],],
        ['ATGCCGCT', 'T', [(1,2),(7,8)],],
        ['ATGCCGCT', '', [],],
        ['TAAAT', 'AA', [(1,3)],],
    )
    @unpack
    def test_search_sub_seq(self, seq, sub_seq, expect):
        res = Seq(seq).search_sub_seq(sub_seq)
        assert res == expect

    @data(
        ['ATGC', 'ATGC', 0],
        ['ATGC', 'ATTC', 1],
        ['ATGC', 'CTAG', 3],
        ['AAACCCGGGTTT', 'CGACGATATGTC', 9],
        ['ATGC', 'AT', 2],
        ['ATGC', 'ATGCT', 1],
    )
    @unpack
    def test_calculate_hamming_distance(self, seq1, seq2, expect):
        res = Seq(seq1).calculate_hamming_distance(seq2)
        assert res == expect

    @data(
        ['ATGC', 'ATGC', 1],
        ['ATGC', 'ATTC', .75],
        ['ATGC', 'CTAG', .25],
        ['ATGC', 'GGAT', 0],
        ['AAACCCGGGTTT', 'CGACGATATGTC', .25],
    )
    @unpack
    def test_calculate_similarity(self, seq1, seq2, expect):
        res = Seq(seq1).calculate_similarity(seq2)
        assert res == expect

