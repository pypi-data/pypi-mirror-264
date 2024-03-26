from tests.helper import *

from src.biofile import FastaDNA, GFF, AnnotValidate





class TestValidate(TestCase):

    def test_demo_RNA(self):
        infiles = [os.path.join(DIR_DATA, 'ncbi_genome_rna.fna'),]
        res = FastaDNA(infiles, DIR_TMP).ncbi_rna_dna()
        fa_file = res['outfile']
        infile = os.path.join(DIR_DATA, 'human_genomic.gff')
        res = GFF(infile, DIR_TMP).retrieve_transcript()
        json_file = res['outfile']
        res = AnnotValidate.ID_fasta_vs_json(fa_file, json_file)
        assert res == (0, 2376, 21)

    @skip
    def test_genome_RNA(self):
        infiles = [os.path.join(DIR_TMP, 'GCF_000001405.40_GRCh38.p14_rna.fna'),]
        res = FastaDNA(infiles, DIR_TMP).ncbi_rna_dna()
        fa_file = res['outfile']
        infile = os.path.join(DIR_TMP, 'GCF_000001405.40_GRCh38.p14_genomic.gff')
        res = GFF(infile, DIR_TMP).retrieve_RNA()
        json_file = res['outfile']
        res = AnnotValidate.ID_fasta_vs_json(fa_file, json_file)

    @skip
    def test_genome_mRNA(self):
        infiles = [os.path.join(DIR_TMP, 'GCF_000001405.40_GRCh38.p14_rna.fna'),]
        res = FastaDNA(infiles, DIR_TMP).ncbi_rna_dna('mRNA')
        fa_file = res['outfile']
        infile = os.path.join(DIR_TMP, 'GCF_000001405.40_GRCh38.p14_genomic.gff')
        res = GFF(infile, DIR_TMP).retrieve_mRNA()
        json_file = res['outfile']
        res = AnnotValidate.ID_fasta_vs_json(fa_file, json_file)
        assert res == (136181, 89, 0)

    @skip
    def test_genome_CDS(self):
        infiles = [os.path.join(DIR_TMP, 'GCF_000001405.40_GRCh38.p14_cds_from_genomic.fna'),]
        res = FastaDNA(infiles, DIR_TMP).ncbi_cds()
        fa_file = res['outfile']
        infile = os.path.join(DIR_TMP, 'GCF_000001405.40_GRCh38.p14_genomic.gff')
        res = GFF(infile, DIR_TMP).retrieve_CDS()
        json_file = res['outfile']
        res = AnnotValidate.ID_fasta_vs_json(fa_file, json_file)
        assert res == (136194, 8260, 0)

    @skip      
    def test_genome_pseudo(self):
        infiles = [os.path.join(DIR_TMP, 'GCF_000001405.40_GRCh38.p14_pseudo_without_product.fna'),]
        res = FastaDNA(infiles, DIR_TMP).ncbi_pseudo()
        fa_file = res['outfile']
        infile = os.path.join(DIR_TMP, 'GCF_000001405.40_GRCh38.p14_genomic.gff')
        res = GFF(infile, DIR_TMP).retrieve_pseudo()
        json_file = res['outfile']
        res = AnnotValidate.ID_fasta_vs_json(fa_file, json_file)
        assert res == (17649, 0, 1603)
