'''
Test class 
'''
from tests.helper import *
from src.eseq import Palindromic

@ddt
class TestPalindromic(TestCase):


    @data(
        ['GATCTCTAG', True],
        ['GATCCTAG', True],
        ['GAG', True],
        ['GG', True],
        ['GATT', False],
        ['', False],
    )
    @unpack
    def test_is_palindromic(self, input, expect):
        res = Palindromic.is_palindromic(input)
        assert res == expect
    
    @data(
        [
            'GCGCTCCTGATTTAATACGACGAGACGACCAGCCCCAGCCGAGATTTGTGCTGATCCGGT',
            [('GACCAG', 26, 31), ('AGCCGA', 36, 41)],
        ],
    )
    @unpack
    def test_detect_palindromic(self, input, expect):
        res = Palindromic(input).detect_palindromic(6)
        assert res == expect

    @data(
        [
            'GCGCTCCTGATTTAATACGACGAGACGACCAGCCCCAGCCGAGATTTGTGCTGATCCGGT',
            [('CGACCAGC', 25, 32)],
        ],
    )
    @unpack
    def test_detect_longest_palindromic(self, input, expect):
        res = Palindromic(input).detect_longest_palindromic()
        assert res == expect