from tests.helper import *

from src.biofile import Wrap


class TestWrap(TestCase):

    def test_ncbi_fa_gff(self):
        local_files = [
            os.path.join(DIR_DATA, 'ncbi_genome_rna.fna'),
            os.path.join(DIR_TMP, 'GCF_000001405.40_GRCh38.p14_cds_from_genomic.fna'),
            os.path.join(DIR_TMP, 'GCF_000001405.40_GRCh38.p14_pseudo_without_product.fna'),
            os.path.join(DIR_TMP, 'GCF_000001405.40_GRCh38.p14_genomic.gff'),
        ]
        w = Wrap(local_files, DIR_TMP)
        output = w.load_output()
        meta = w.ncbi_fa_gff()
        output = w.save_output(meta, True)
