'''
Test class ORF

Test sequence I:
1-42
0   3   6   9   12  15  18  21  24  27  30  33  36  39 
ATG-ACA-CGA-TAT-GAG-ATA-TGC-ATA-GAA-AGC-GAA-TAT-AGA-TAG

frames:
1: ATG-ACA-CGA-TAT-GAG-ATA-TGC-ATA-GAA-AGC-GAA-TAT-AGA-TAG
2:           ATG-AGA-TAT-GCA-TAG
3:                       ATG-CAT-AGA-AAG-CGA-ATA-TAG
'''
from tests.helper import *
from src.eseq import ORF

@ddt
class TestORF(TestCase):


    @data(
        [10, False, [(0, 42), (10, 25), (17, 38)]],
        [None, True, [(0, 42),]],
        [None, None, [(0, 42),]],
        [50, None, []],
    )
    @unpack
    def test_detect_orfs(self, min_length, ignore_nested, expect):
        seq = 'ATGACACGATATGAGATATGCATAGAAAGCGAATATAGATAG'
        res = ORF(seq, min_length, ignore_nested).detect_orfs()
        assert res == expect

    @data(
        # default min_length=30
        [0, None, ('TAG', 39, 42),],
        # ORFs are in the middle of sequence
        [10, 10, ('TAG', 22, 25),],
        [17, 10, ('TAG', 35, 38),],
        # no termination codon detected
        [17, 50, None,],
    )
    @unpack
    def test_detect_termination_codon(self, start, min_length, expect):
        seq = 'ATGACACGATATGAGATATGCATAGAAAGCGAATATAGATAG'
        res = ORF(seq, min_length=min_length).detect_termination_codon(start)
        assert res == expect

    @data(
        ['ATG', True],
        ['TAC', False],
        ['TAA', False],
    )
    @unpack
    def test_is_start_codon(self, input, expect):
        res = ORF().is_start_codon(input)
        assert res == expect

    @data(
        ['ATG', False],
        ['TAC', False],
        ['TAA', True],
        ['TAG', True],
        ['TGA', True],
    )
    @unpack
    def test_is_termination_codon(self, input, expect):
        res = ORF().is_termination_codon(input)
        assert res == expect

    @data(
        [
            'ATGACACGATATGAGATATGCATAGAAAGCGAATATAGATAG',
            [('ATG', 0, 2), ('ATG', 10, 12), ('ATG', 17, 19)]
        ],
    )
    @unpack
    def test_detect_start_codon(self, input, expect):
        res = ORF(input).detect_start_codon()
        assert list(res) == expect


