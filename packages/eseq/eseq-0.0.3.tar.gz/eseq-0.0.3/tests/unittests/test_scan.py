'''
Test class 
'''
from tests.helper import *
from src.eseq import Scan

@ddt
class TestScan(TestCase):

    @data(
        ['ATC', None, None, [('A', 1), ('T', 2), ('C', 3)]],
        ['ATC', 0, 1, [('A', 1), ('T', 2), ('C', 3)]],
        ['ATC', 0, -2, [('A', 1), ('T', 2), ('C', 3)]],
        ['ATC', 0, 2, [('AT', 2), ('C', 3)]],
        ['ATCG', 0, 2, [('AT', 2), ('CG', 4)]],
        ['ATC', 0, 3, [('ATC',3)]],
        ['ATC', 0, 10, [('ATC',3)]],
        ['ATGACACGATATGAGATATGCATAGAAAGCGAATATAGATAG', 0, 3, [('ATG', 3), 
            ('ACA', 6), ('CGA', 9), ('TAT', 12), ('GAG', 15), ('ATA', 18),
            ('TGC', 21), ('ATA', 24), ('GAA', 27), ('AGC', 30), ('GAA', 33),
            ('TAT', 36), ('AGA', 39), ('TAG', 42)],],
        ['ATGACACGATATGAGATATGCATAGAAAGCGAATATAGATAG',9, 3, [('TAT', 12), \
            ('GAG', 15), ('ATA', 18), ('TGC', 21), ('ATA', 24), ('GAA', 27),\
            ('AGC', 30), ('GAA', 33), ('TAT', 36), ('AGA', 39), ('TAG', 42)],],
    )
    @unpack
    def test_forward(self, seq, start, step, expect):
        res = Scan.forward(seq, start, step)
        assert list(res) == expect

    @data(
        ['ATC', None,  ['C', 'T', 'A']],
        ['ATC', 1,  ['C', 'T', 'A']],
        ['ATC', -2,  ['C', 'T', 'A']],
        ['ATC', 2,  ['TC', 'A']],
        ['ATCG', 2,  ['CG', 'AT']],
        ['ATC', 3,  ['ATC']],
        ['ATC', 10,  ['ATC']],
    )
    @unpack
    def test_backward(self, seq, step, expect):
        res = Scan.backward(seq, step)
        assert list(res) == expect

    @data(
        ['ATC', None,  [('A', 'T'), ('T', 'C')]],
        ['ATCG', 1,  [('A', 'T'), ('T', 'C'), ('C', 'G')]],
        ['ATC', 2,  [('AT', 'TC'),]],
    )
    @unpack
    def test_neighbor_forward(self, seq, step, expect):
        res = Scan.neighbor_forward(seq, step)
        assert list(res) == expect

    @data(
        ['ATC', [('A','C')]],
        ['AC', [('A','C')]],
        ['A', []],
        ['', []],
        ['ATGCACC', [('A','C'),('T','C'),('G','A')]],
    )
    @unpack
    def test_biends(self, seq, expect):
        res = Scan.biends(seq)
        assert list(res) == expect

    @data(
        ['ATACTC', 5, None, ['ATACT', 'TACTC']],
        ['ATACTC', 15, None, ['ATACTC']],
        ['ATA', 1, None, ['A','T','A',]],
        ['ATCGG', 2, None, ['AT', 'TC', 'CG', 'GG']],
        ['ATCGG', 3, None, ['ATC', 'TCG', 'CGG']],
        ['ATCGG', 6, None, ['ATCGG']],
        ['ATCGG', 3, 2, ['CGG']],
        ['ATCGG', 3, -4, ['TCG', 'CGG']],
    )
    @unpack
    def test_k_mers(self, seq, k, start, expect):
        res = Scan.k_mers(seq, k, start)
        assert [i[0] for i in res] == expect