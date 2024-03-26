from tests.helper import *
from src.biofile import AnnotRecord

GFF_LINE = "sequence001	mine	CDS	190	252	.	+	0	ID=CDS0;Parent=gene0;Dbxref=UniProtKB/Swiss-Prot:P0AD86;product=formate dehydrogenase isoform 1;transl_except=(pos:193..195%2Caa:Sec);inference=COORDINATES:similar to AA sequence:INSD:AAC73526.1"
NO_ATTR = "sequence001	mine	CDS	190	252	.	+	0"

GTF_LINE = '''381\tTwinscan\tCDS\t380\t401\t.\t+\t0\tgene_id "001"; transcript_id "001.1";'''

@ddt
class TestAnnotRecord(TestCase):

    def test_parse_gff(self):
        c = AnnotRecord()
        c.parse(GFF_LINE)
        assert c.seqid == 'sequence001'
        assert c.source == 'mine'
        assert c.feature == 'CDS'
        assert c.start == 190
        assert c.end == 252
        assert c.score == '.'
        assert c.strand == '+'
        assert c.phase == '0'
        assert c.attributes == 'ID=CDS0;Parent=gene0;Dbxref=UniProtKB/Swiss-Prot:P0AD86;product=formate dehydrogenase isoform 1;transl_except=(pos:193..195%2Caa:Sec);inference=COORDINATES:similar to AA sequence:INSD:AAC73526.1'

    def test_to_dict_gff(self):
        c = AnnotRecord()
        res = c.to_dict()
        assert res == {'seqid': None, 'source': None, 'feature': None, 'start': None, \
            'end': None, 'score': None, 'strand': None, 'phase': None, 'attributes': None}
        
        c.parse(GFF_LINE)
        res = c.to_dict()
        assert res == {'seqid': 'sequence001', 'source': 'mine', 'feature': 'CDS', \
            'start': 190, 'end': 252, 'score': '.', 'strand': '+', 'phase': '0', 'attributes': \
            'ID=CDS0;Parent=gene0;Dbxref=UniProtKB/Swiss-Prot:P0AD86;product=formate dehydrogenase isoform 1;transl_except=(pos:193..195%2Caa:Sec);inference=COORDINATES:similar to AA sequence:INSD:AAC73526.1'}

    def test_parse_gtf(self):
        c = AnnotRecord()
        c.parse(GTF_LINE)
        assert c.seqid == '381'
        assert c.source == 'Twinscan'
        assert c.feature == 'CDS'
        assert c.start == 380
        assert c.end == 401
        assert c.score == '.'
        assert c.strand == '+'
        assert c.phase == '0'
        assert c.attributes == 'gene_id "001"; transcript_id "001.1";'

        res = c.to_dict()
        assert res == {'seqid': '381', 'source': 'Twinscan', 'feature': 'CDS', 'start': 380, \
            'end': 401, 'score': '.', 'strand': '+', 'phase': '0', \
            'attributes': 'gene_id "001"; transcript_id "001.1";'}

    def test_other_record_line(self):
        c = AnnotRecord()
        c.parse('')
        assert c.seqid == ''
        assert c.source == None
        c.parse('abc')
        assert c.seqid == 'abc'
        assert c.source == None
        
        # 8 columns
        c.parse(NO_ATTR)
        assert c.seqid == 'sequence001'
        assert c.source == 'mine'
        assert c.feature == 'CDS'
        assert c.start == 190
        assert c.end == 252
        assert c.score == '.'
        assert c.strand == '+'
        assert c.phase == '0'
        assert c.attributes == None 

    @data(
        [
            'gene_id "001"; transcript_id "001.1";',
            [{'name': 'gene_id', 'value': '001'}, {'name': 'transcript_id', 'value': '001.1'}],
        ],
        [
            '''gene_id "DDX11L1"; transcript_id ""; db_xref "GeneID:100287102"; db_xref "HGNC:HGNC:37102"; description "DEAD/H-box helicase 11 like 1 (pseudogene)"; gbkey "Gene"; gene "DDX11L1"; gene_biotype "transcribed_pseudogene"; pseudo "true";''',
            [{'name': 'gene_id', 'value': 'DDX11L1'}, {'name': 'transcript_id', 'value': ''}, \
            {'name': 'db_xref', 'value': 'GeneID:100287102'}, {'name': 'db_xref', 'value': 'HGNC:HGNC:37102'}, \
            {'name': 'description', 'value': 'DEAD/H-box helicase 11 like 1 (pseudogene)'}, \
            {'name': 'gbkey', 'value': 'Gene'}, {'name': 'gene', 'value': 'DDX11L1'}, \
            {'name': 'gene_biotype', 'value': 'transcribed_pseudogene'}, {'name': 'pseudo', 'value': 'true'}],
        ],
        [
            '''gene_id "LOC124900384"; transcript_id "XR_001737579.3"; db_xref "GeneID:124900384"; gbkey "ncRNA"; gene "LOC124900384"; model_evidence "Supporting evidence includes similarity to: 5 long SRA reads, and 78% coverage of the annotated genomic feature by RNAseq alignments, including 34 samples with support for all annotated introns"; product "uncharacterized LOC124900384, transcript variant X13"; transcript_biotype "lnc_RNA";''',
            [{'name': 'gene_id', 'value': 'LOC124900384'}, {'name': 'transcript_id', 'value': 'XR_001737579.3'}, \
            {'name': 'db_xref', 'value': 'GeneID:124900384'}, {'name': 'gbkey', 'value': 'ncRNA'}, \
            {'name': 'gene', 'value': 'LOC124900384'}, {'name': 'model_evidence', 'value': 'Supporting evidence includes similarity to: 5 long SRA reads, and 78% coverage of the annotated genomic feature by RNAseq alignments, including 34 samples with support for all annotated introns'}, \
            {'name': 'product', 'value': 'uncharacterized LOC124900384, transcript variant X13'}, \
            {'name': 'transcript_biotype', 'value': 'lnc_RNA'}],
        ],
    )
    @unpack
    def test_parse_gtf_attributes(self, input, expect):
        res = AnnotRecord.parse_gtf_attributes(input)
        assert res == expect

    @data(
        [
            'ID=gene5',
            [{'name': 'ID', 'value': 'gene5'}],
        ],
        [
            'ID=rrna1;Parent=gener1;product=18S ribosomal RNA',
            [{'name': 'ID', 'value': 'rrna1'}, {'name': 'Parent', 'value': 'gener1'}, \
            {'name': 'product', 'value': '18S ribosomal RNA'}]
        ],
        [
            'ID=CDS0;Parent=gene0;Dbxref=UniProtKB/Swiss-Prot:P0AD86;product=formate dehydrogenase isoform 1;transl_except=(pos:193..195%2Caa:Sec);inference=COORDINATES:similar to AA sequence:INSD:AAC73526.1',
            [{'name': 'ID', 'value': 'CDS0'}, {'name': 'Parent', 'value': 'gene0'}, \
            {'name': 'Dbxref', 'value': 'UniProtKB/Swiss-Prot:P0AD86'}, \
            {'name': 'product', 'value': 'formate dehydrogenase isoform 1'}, \
            {'name': 'transl_except', 'value': '(pos:193..195%2Caa:Sec)'}, \
            {'name': 'inference', 'value': 'COORDINATES:similar to AA sequence:INSD:AAC73526.1'}]
        ],
        [
            'ID=id070000;Note=RIP1 (repetitive extragenic palindromic) element%3B contains 2 REP sequences and 1 IHF site;',
            [{'name': 'ID', 'value': 'id070000'}, {'name': 'Note', 'value': \
            'RIP1 (repetitive extragenic palindromic) element%3B contains 2 REP sequences and 1 IHF site'}]  
        ],
        [
            '''ID=CDS2;Parent=gene2;Dbxref=UniProtKB/Swiss-Prot:P00547,InterPro:IPR002928;product=2'%2C3'-cyclic phosphodiesterase;ec_number=2.7.7.1,2.7.1.22;''',
            [{'name': 'ID', 'value': 'CDS2'}, {'name': 'Parent', 'value': 'gene2'}, \
            {'name': 'Dbxref', 'value': 'UniProtKB/Swiss-Prot:P00547'}, {'name': 'Dbxref', 'value': 'InterPro:IPR002928'},\
            {'name': 'product', 'value': "2'%2C3'-cyclic phosphodiesterase"}, \
            {'name': 'ec_number', 'value': '2.7.7.1,2.7.1.22'}]
        ],
        [
            '''ID=exon-NR_024540.1-4;Parent=rna-NR_024540.1;Dbxref=GeneID:653635,GenBank:NR_024540.1,HGNC:HGNC:38034;gbkey=misc_RNA;gene=WASH7P;product=WASP family homolog 7%2C pseudogene;pseudo=true;transcript_id=NR_024540.1''',
            [{'name': 'ID', 'value': 'exon-NR_024540.1-4'}, {'name': 'Parent', 'value': 'rna-NR_024540.1'}, \
            {'name': 'Dbxref', 'value': 'GeneID:653635'}, {'name': 'Dbxref', 'value': 'GenBank:NR_024540.1'}, \
            {'name': 'Dbxref', 'value': 'HGNC:HGNC:38034'}, {'name': 'gbkey', 'value': 'misc_RNA'}, \
            {'name': 'gene', 'value': 'WASH7P'}, {'name': 'product', 'value': 'WASP family homolog 7%2C pseudogene'}, \
            {'name': 'pseudo', 'value': 'true'}, {'name': 'transcript_id', 'value': 'NR_024540.1'}]
        ],
        [
            '''ID=id-GeneID:127266744;Dbxref=GeneID:127266744;Note=OCT4-NANOG hESC enhancer chr1:569139-570114 (GRCh37/hg19 assembly coordinates);experiment=EXISTENCE:reporter gene assay evidence [ECO:0000049][PMID:30033119];function=activates a minimal SCP1%2C AML or CMV promoter by ChIP-STARR-seq in naive and primed H9 embryonic stem cells {active_cell/tissue: H9 hESC(naive and primed)};gbkey=regulatory;regulatory_class=enhancer''',
            [{'name': 'ID', 'value': 'id-GeneID:127266744'}, {'name': 'Dbxref', 'value': 'GeneID:127266744'}, \
            {'name': 'Note', 'value': 'OCT4-NANOG hESC enhancer chr1:569139-570114 (GRCh37/hg19 assembly coordinates)'}, \
            {'name': 'experiment', 'value': 'EXISTENCE:reporter gene assay evidence [ECO:0000049][PMID:30033119]'}, \
            {'name': 'function', 'value': 'activates a minimal SCP1%2C AML or CMV promoter by ChIP-STARR-seq in naive and primed H9 embryonic stem cells {active_cell/tissue: H9 hESC(naive and primed)}'}, \
            {'name': 'gbkey', 'value': 'regulatory'}, {'name': 'regulatory_class', 'value': 'enhancer'}]
        ],
    )
    @unpack
    def test_parse_gff_attributes(self, input, expect):
        res = AnnotRecord.parse_gff_attributes(input)
        assert res == expect