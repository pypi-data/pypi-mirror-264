'''
Test class 
'''
from tests.helper import *
from src.eseq import BioDNA

@ddt
class TestBioDNA(TestCase):

    @data(
        ['ATGC', None, 4],
        [None, 20, 20],
    )
    @unpack
    def test_(self, data, length, expect_length):
        c = BioDNA(data, length)
        assert c.__len__() == expect_length
    
    def test_count_subseq(self):
        res = BioDNA('ATGATCTA').count('AT')
        assert res == 2

    def test_locate_subseq(self):
        res = BioDNA('GATCTA').find('AT')
        assert res == 1

    def test_complement(self):
        res = BioDNA('GATCTA').complement()
        assert res == 'CTAGAT'

    def test_reverse_complement(self):
        res = BioDNA('GATCTA').reverse_complement()
        assert res == 'TAGATC'

    @data(
        ['GATCTA', None, 'DL'],
        ["ATGGCCATTGTAATGGGCCGCTGAAAGGGTGCCCGATAG", None, 'MAIVMGR*KGAR*'],
        ["ATGGCCATTGTAATGGGCCGCTGAAAGGGTGCCCGATAG", True, 'MAIVMGR'],
        ['AT', None, ''],
    )
    @unpack
    def test_to_protein(self, seq, to_stop, expect):
        res = BioDNA(seq).translate(to_stop=to_stop)
        assert res == expect

    def test_to_rna(self):
        res = BioDNA('GATCTA').transcribe()
        assert res == 'GAUCUA'
    
    @data(
        ['ATCG', {'A': '0001', 'T': '0010', 'C': '0100', 'G': '1000'} ],
        ['nina', {'n': '0101', 'i': '0010', 'a': '1000'}],
    )
    @unpack
    def test_to_mask(self, input, expect):
        _, res = BioDNA(input).nt_bitvector()
        assert res == expect

    @data(
        ['cdd', 'acdd', [1,]],
        ['nina', 'ninjaninaaninann', [5, 10]],
        ['cdc', 'acddcd', []],
        ['cdc', 'cdc', [0]],
        ['cdc', 'acdcdc', [1,3]],
        ['NNN', 'NNNNN', [0,1,2]]
    )
    @unpack
    def test_shift_and(self, pattern, text, expect):
        res = BioDNA(pattern).shift_and(text)
        assert res == expect
        