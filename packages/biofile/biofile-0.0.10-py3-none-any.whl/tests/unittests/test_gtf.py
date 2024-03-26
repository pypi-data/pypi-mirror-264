from tests.helper import *

from src.biofile import GTF

@ddt
class TestGTF(TestCase):

    @data(
        ['human_genomic.gtf', 9995],
    )
    @unpack
    def test_iterator(self, file_name, expect):
        gtf_file = os.path.join(DIR_DATA, file_name)
        iter = GTF(gtf_file).iterator()
        res = [i for i in iter]
        assert len(res) == expect

    def test_split(self):
        gtf_file = os.path.join(DIR_DATA, 'human_genomic.gtf')
        # statistics
        res = GTF(gtf_file).split_by_feature()
        assert res['transcript'] == 465
        
        # export to json
        res = GTF(gtf_file, DIR_TMP).split_by_feature()
        assert res['transcript'] == os.path.join(DIR_TMP, "transcript.json")

        # decompose attributes
        res = GTF(gtf_file, DIR_TMP).split_by_feature(True)


    @data(
        ['gene_id', None, 143],
        ['gene_id', '_all_', 143],
        ['gene_id', 'CDS', 55],
        ['gene_id', 'transcript', 115],
        ['gene', 'transcript', 179],
        ['ID', 'wrong', 0],
        ['wrong', None, 0],
    )
    @unpack
    def test_parse_attributes(self, attr, feature, expect):
        gff_file = os.path.join(DIR_DATA, 'human_genomic.gtf')
        res = GTF(gff_file, DIR_TMP).parse_attributes(attr, feature)
        assert len(res) == expect

    @data(
        ['gene_id', 'MIR6859-1', {'seqid': 'NC_000001.11', 'source': 'BestRefSeq', \
            'feature': 'gene', 'start': 17369, 'end': 17436, 'score': '.', 'strand': '-', 'phase': '.', \
            'attributes': 'gene_id "MIR6859-1"; transcript_id ""; db_xref "GeneID:102466751"; db_xref "HGNC:HGNC:50039"; db_xref "miRBase:MI0022705"; description "microRNA 6859-1"; gbkey "Gene"; gene "MIR6859-1"; gene_biotype "miRNA"; gene_synonym "hsa-mir-6859-1";', \
            'ID': 'MIR6859-1'}],
        ["GeneID", "GeneID:102466751", {'seqid': 'NC_000001.11', 'source': 'BestRefSeq', \
            'feature': 'gene', 'start': 17369, 'end': 17436, 'score': '.', 'strand': '-', 'phase': '.', \
            'attributes': 'gene_id "MIR6859-1"; transcript_id ""; db_xref "GeneID:102466751"; db_xref "HGNC:HGNC:50039"; db_xref "miRBase:MI0022705"; description "microRNA 6859-1"; gbkey "Gene"; gene "MIR6859-1"; gene_biotype "miRNA"; gene_synonym "hsa-mir-6859-1";', \
            'ID': 'GeneID:102466751'}],
    )
    @unpack
    def test_lift_attributes(self, attr, key, expect):
        infile = os.path.join(DIR_DATA, 'gtf_gene.json')
        res = GTF(infile).lift_attribute(attr)
        assert res[key] == expect

    