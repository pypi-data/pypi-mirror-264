from tests.helper import *

from src.biofile import GFF

@ddt
class TestGFF(TestCase):
    '''
    @data(
        ['human_genomic.gff', 9991],
    )
    @unpack
    def test_iterator(self, file_name, expect):
        gff_file = os.path.join(DIR_DATA, file_name)
        iter = GFF(gff_file).iterator()
        res = [i for i in iter]
        assert len(res) == expect

    def test_split(self):
        gff_file = os.path.join(DIR_DATA, 'human_genomic.gff')
        # statistics
        res = GFF(gff_file).split_by_feature()
        assert res['transcript'] == 21
        
        # export to json
        res = GFF(gff_file, DIR_TMP).split_by_feature()
        assert res['transcript'] == os.path.join(DIR_TMP, "transcript.json")

        # attributes
        res = GFF(gff_file, DIR_TMP).split_by_feature(True)
    
    @data(
        ['ID', None, 6467],
        ['ID', '_all_', 6467],
        ['ID', 'CDS', 333],
        ['ID', 'mRNA', 334],
        ['gene', 'mRNA', 55],
        ['transcript_id', 'mRNA', 334],
        ['ID', 'wrong', 0],
        ['wrong', None, 0],
    )
    @unpack
    def test_parse_attributes(self, attr, feature, expect):
        gff_file = os.path.join(DIR_DATA, 'human_genomic.gff')
        res = GFF(gff_file, DIR_TMP).parse_attributes(attr, feature)
        assert len(res) == expect

    @data(
        ['ID', 'gene-TRNT', {'seqid': 'NC_012920.1', 'source': 'RefSeq', 'feature': 'gene', \
            'start': 15888, 'end': 15953, 'score': '.', 'strand': '+', 'phase': '.', 
            'attributes': 'ID=gene-TRNT;Dbxref=GeneID:4576,HGNC:HGNC:7499,MIM:590090;Name=TRNT;gbkey=Gene;gene=TRNT;gene_biotype=tRNA;gene_synonym=MTTT',\
            'ID': 'gene-TRNT'}],
        ['GeneID', 'GeneID:4576', {'seqid': 'NC_012920.1', 'source': 'RefSeq', 'feature': 'gene', \
            'start': 15888, 'end': 15953, 'score': '.', 'strand': '+', 'phase': '.', 
            'attributes': 'ID=gene-TRNT;Dbxref=GeneID:4576,HGNC:HGNC:7499,MIM:590090;Name=TRNT;gbkey=Gene;gene=TRNT;gene_biotype=tRNA;gene_synonym=MTTT',\
            'ID': 'GeneID:4576'}],
    )
    @unpack
    def test_lift_attributes(self, name, key, expect):
        infile = os.path.join(DIR_DATA, 'gff_gene.json')
        res = GFF(infile).lift_attribute(name)
        assert res[key] == expect
    '''

    def test_retrieve_mRNA(self):
        infile = os.path.join(DIR_DATA, 'human_genomic.gff')
        res = GFF(infile, DIR_TMP).retrieve_mRNA()
        assert res.get('records') == 334

    def test_retrieve_CDS(self):
        infile = os.path.join(DIR_DATA, 'human_genomic.gff')
        res = GFF(infile, DIR_TMP).retrieve_CDS()
        assert res.get('records') == 333

    def test_retrieve_pseudo(self):
        infile = os.path.join(DIR_DATA, 'human_genomic.gff')
        res = GFF(infile, DIR_TMP).retrieve_pseudo()
        assert res.get('records') == 34

    def test_retrieve_transcript(self):
        infile = os.path.join(DIR_DATA, 'human_genomic.gff')
        res = GFF(infile, DIR_TMP).retrieve_transcript()
        assert res.get('records') == 21

    def test_retrieve_mRNA(self):
        infile = os.path.join(DIR_DATA, 'human_genomic.gff')
        res = GFF(infile, DIR_TMP).retrieve_mRNA()
        assert res.get('records') == 334