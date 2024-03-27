"""
data structure: The di-trie. Here are the features:
Define A trie and B trie:
one leave node of A trie is mapped to one or more leave nodes of B trie
"""
from .utils.file import File
from .utils.constants import *

from .trie import Trie
from .ditrie import DiTrie

class ProcessID:
    
    def uniprotkb_protein_accession(self, infile:str)->Trie:
        """
        source file: gene_refseq_uniprotkb_collab downloaded from NCBI/Entrez
        suck UniProtKB protein accession numbers
        """
        acc_trie = Trie()
        n = 0
        for items in File(infile).read_text(True, '\t'):
            acc = items[1]
            acc_trie.insert(acc)
            n += 1
        print(f"Total number of {n} UniProtKB protein accession numbers are fed into Trie.")
        return acc_trie

    def ncbi_protein_accession(self, infile:str)->Trie:
        """
        source file: gene_refseq_uniprotkb_collab downloaded from NCBI/Entrez
        suck NCBI protein accession numbers
        """
        acc_trie = Trie()
        n = 0
        for items in File(infile).read_text(True, '\t'):
            acc = items[0]
            acc_trie.insert(acc)
            n += 1
        print(f"Total number of {n} NCBI protein accession numbers are fed into Trie.")
        return acc_trie


    def map_ncbi_uniprotkb(self, infile:str)->DiTrie:
        '''
        source file: gene_refseq_uniprotkb_collab downloaded from NCBI/Entrez
        map: UniProtKB accession number ~ NCBI protein accession number
        '''
        uniprotkb_acc_trie = Trie()
        ncbi_acc_trie = Trie()
        map_trie = DiTrie(uniprotkb_acc_trie, ncbi_acc_trie)

        n = 0
        for items in File(infile).read_text(True, '\t'):
            ncbi_acc, uniprotkb_acc = items[:2]
            map_trie.insert(ncbi_acc, uniprotkb_acc)
            n += 1
        return map_trie
    

