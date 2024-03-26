'''
Test class 
'''
from tests.helper import *
from src.eseq import Prosite

@ddt
class TestProsite(TestCase):

    @data(
        # N-glycosylation site
        ['N-{P}-[ST]-{P}', (4,4)],
        ['[EDQH]-x-K-x-[DN]-G-x-R-[GACV]', (9,9)],
        ['RGD', (3,3)],
        ['[LIVM]-R-x(2)-P-D-x-[LIVM](3)-G-E-[LIVM]-R-D', (15,15)],
        ['C-x(2)-P-F-x-[FYWIV]-x(7)-C-x(8,10)-W', (24,26)],
    )
    @unpack
    def test_motif_lenght(self, prosite, expect):
        res = Prosite(prosite).motif_length()
        assert res == expect
    
    @data(
        ['N-{P}-[ST]-{P}', 'N[^P][ST][^P]'],
        ['[AC]-x-V-x(4)-{ED}', '[AC]\wV\w{4}[^ED]'],
        ['<A-x-[ST](2)-x(0,1)-V', '^A\w[ST]{2}\w{0,1}V'],
    )
    @unpack
    def test_compile_prosite(self, input, expect):
        res = Prosite(input).compile_prosite()
        assert getattr(res, 'pattern') == expect
    
    @data(
        # N-glycosylation
        ['N-{P}-[ST]-{P}', 'EYQTRQDQCIYNTTYLNVQREN', [(11, 15, 'NTTY')] ],
        ['N-{P}-[ST]-{P}', 'EYLTIGNQCVYNSSYLNVQR', [(11, 15, 'NSSY')] ],
    )
    @unpack
    def test_detect_1(self, prosite, input, expect):
        c = Prosite(prosite)
        c.compile_prosite()
        res = c.search_motif(input)
        assert res == expect