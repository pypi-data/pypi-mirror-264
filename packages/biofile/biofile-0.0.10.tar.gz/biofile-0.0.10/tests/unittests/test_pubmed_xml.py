'''
Test class 
'''
from tests.helper import *
from src.biofile.pubmed_xml import PubmedXml


@ddt
class Test_(TestCase):

    def setUp(self):
        infile = os.path.join(DIR_DATA, 'pubmed23n0001.xml')
        self.c = PubmedXml(infile)

    def test_parse_xml(self):
        self.c.parse_xml()
