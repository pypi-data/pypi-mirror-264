'''
Test Tree
'''
from .helper import *
from src.parseID import ProcessID

@ddt
class TestTrie(TestCase):

    def test_retrieve_uniprotkb_accession(self):
        infile = os.path.join(DIR_DATA, 'gene_refseq_uniprotkb_collab')
        uniprotkb_acc_trie = ProcessID().uniprotkb_protein_accession(infile)
        res = uniprotkb_acc_trie.dump()
        assert len(res) == 822535

    def test_retrieve_ncbi_accession(self):
        infile = os.path.join(DIR_DATA, 'gene_refseq_uniprotkb_collab')
        ncbi_acc_trie = ProcessID().ncbi_protein_accession(infile)
        res = ncbi_acc_trie.dump()
        assert len(res) == 448595

    def test_ditrie(self):
        infile = os.path.join(DIR_DATA, 'gene_refseq_uniprotkb_collab')
        ncbi_uniprotkb_ditrie = ProcessID().map_ncbi_uniprotkb(infile)
        res = [i for i in ncbi_uniprotkb_ditrie.items()]
        assert len(res) == 448595
