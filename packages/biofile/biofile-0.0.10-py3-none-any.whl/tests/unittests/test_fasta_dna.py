'''
'''
from tests.helper import *
from src.biofile import FastaDNA

@ddt
class TestFastaDNA(TestCase):

    @data(
        ['mRNA', 2376],
        [None, 2376],
    )
    @unpack
    def test_ncbi_rna_dna(self, input, expect):
        infiles = [os.path.join(DIR_DATA, 'ncbi_genome_rna.fna'),]
        res = FastaDNA(infiles, DIR_TMP).ncbi_rna_dna(input)
        assert res['records'] == expect
   
    def test_ncbi_cds(self):
        infiles = [os.path.join(DIR_DATA, 'ncbi_cds_from_genomic.fna'),]
        res = FastaDNA(infiles, DIR_TMP).ncbi_cds()
        assert res['records'] == 469

    def test_ncbi_pseudo(self):
        infiles = [os.path.join(DIR_DATA, 'ncbi_pseudo_without_product.fna'),]
        res = FastaDNA(infiles, DIR_TMP).ncbi_pseudo()
        assert res['records'] == 556
