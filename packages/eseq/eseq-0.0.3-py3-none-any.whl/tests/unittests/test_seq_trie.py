'''
Test class 
'''
from tests.helper import *
from src.eseq import SeqTrie

@ddt
class TestSeqTrie(TestCase):

    @data(
        ['ATCG', 'G', 4, ()],
        ['A', 'A', 1, ()],
    )
    @unpack
    def test_insert(self, input, expect_val, expect_depth, expect_pos):
        res = SeqTrie().insert(input)
        assert res.val == expect_val
        assert res.depth == expect_depth
        assert getattr(res, 'val_pos') == expect_pos
        assert res.is_leave is True

    @data(
        ['ATCG', 'ATCG'],
    )
    @unpack
    def test_get(self, input, expect):
        leave_node = SeqTrie().insert(input)
        res = SeqTrie().get(leave_node)
        assert res == expect
