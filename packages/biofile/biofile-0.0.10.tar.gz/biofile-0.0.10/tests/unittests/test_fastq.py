'''
Test class 
'''
from tests.helper import *
# from Bio import SeqIO, Seq, SeqRecord
from src.biofile.fastq import FASTQ


@ddt
class Test_(TestCase):

    @data(
        ['1_control_18S_2019_minq7.fastq'],
        ['left.fastq'],
    )
    @unpack
    @mock.patch.dict(os.environ, {'DIR_DATA': DIR_DATA})
    def test_parse_records(self, input):
        fq_file = os.path.join(DIR_DATA, input)
        iter = FASTQ().parse_records(fq_file)
        res = next(iter)
        assert len(res.seq) > 50


    @data(
        ['left.fastq', 'right.fastq'],
    )
    @unpack
    def test_parse_pair_records(self, fq1_file, fq2_file):
        f1 = os.path.join(DIR_DATA, fq1_file)
        f2 = os.path.join(DIR_DATA, fq2_file)
        iter = FASTQ().parse_pair_records(f1, f2)
        res = next(iter)
        assert len(res[0].seq) > 50


    @data(
        ['left.fastq'],
    )
    @unpack
    @mock.patch.dict(os.environ, {'DIR_DATA': DIR_DATA, 'DIR_CACHE': DIR_TMP})
    def test_quality_scores(self, input):
        infile = os.path.join(DIR_DATA, input)
        iter = FASTQ().parse_records(infile)
        FASTQ().quality_scores(iter)

    @data(
        ['left.fastq', True],
        ['left.fq', True],
        ['wrong', False],
        ['dna.fa', False],
    )
    @unpack
    @mock.patch.dict(os.environ, {'DIR_CACHE': DIR_TMP})
    def test_is_fastq(self, input, expect):
        infile = os.path.join(DIR_DATA, input)
        res = FASTQ().is_fastq(infile)
        assert res == expect