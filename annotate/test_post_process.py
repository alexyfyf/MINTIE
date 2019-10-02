import pytest
import pandas as pd
import post_process as pp

@pytest.mark.parametrize('gene,expected', [('A', ['A']),
                                            ('A|B', ['A', 'B']),
                                            ('A:B', ['A', 'B']),
                                            ('A:B|C', ['A', 'B', 'C'])])
def test_get_all_genes(gene, expected):
    pp.get_all_genes(gene) == expected

def test_filter_by_gene():
    gene_filter = {0: ['B', 'C', 'E', 'X']}
    gene_filter = pd.DataFrame.from_dict(gene_filter)

    contigs = {'overlapping_genes': ['A', 'A:B', 'C|E', 'Y', 'X']}
    contigs = pd.DataFrame.from_dict(contigs)

    result = pp.filter_by_gene(contigs, gene_filter).overlapping_genes.values
    assert list(result) == ['A:B', 'C|E', 'X']

@pytest.mark.parametrize('gene,expected', [('A', 'A'),
                                           ('A|B', 'A'),
                                           ('A:B', 'A|B'),
                                           ('A|B|C:X|Y|Z', 'A|X')])
def test_get_short_gene_name(gene, expected):
    assert pp.get_short_gene_name(gene) == expected

def test_make_junctions():
    st_blocks = {'start': [100, 200, 300],
                 'end': [150, 202, 311]}
    st_blocks = pd.DataFrame.from_dict(st_blocks)
    result = {'start': [100, 150, 200, 300, 311],
              'end': [100, 150, 202, 300, 311]}
    result = pd.DataFrame.from_dict(result)
    juncs = pp.make_junctions(st_blocks).sort_values('start').reset_index(drop=True)
    assert all(result == juncs)