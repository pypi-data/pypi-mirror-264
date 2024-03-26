'''
'''
from tests.helper import *
from src.biofile import GBK

@ddt
class TestGBK(TestCase):


    @data(
        ['mRNA', 31],
        [None, 31],
    )
    @unpack
    def test_ncbi_rna_gbk(self, input, expect):
        infiles = [os.path.join(DIR_DATA, 'ncbi_genome_rna.gbff'),]
        res = GBK(infiles, DIR_TMP).ncbi_rna_gbk(input)
        assert res['records'] == expect
    
