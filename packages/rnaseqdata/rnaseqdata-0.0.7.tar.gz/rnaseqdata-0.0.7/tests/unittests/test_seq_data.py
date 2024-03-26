import numpy as np
import pandas as pd
from unittest import TestCase
from ddt import ddt, data, unpack
from src.rnaseqdata import RootData, SeqData

from tests.data.constants import *

@ddt
class TestSeqData(TestCase):

    def test_data_names(self):
        root = RootData(samples, annot)
        c = SeqData(root)
        assert c.data_names() == []
        c.put_data('test1', None, root)
        c.put_data('test2', None)
        assert c.data_names() == ['test1', 'test2']

    def test_get_node_data(self):
        root = RootData(samples, annot)
        c = SeqData(root)
        node = c.get_node_data('test')
        assert node == None

        node1 = c.put_data('test1', None, root)
        node2 = c.put_data('test2', None)
        node = c.get_node_data('test1')
        assert node == node1
        node = c.get_node_data('test2')
        assert node == node2

    @data(
        [RootData(samples, annot),],
        [RootData(None, None),],
        [None,],
    )
    @unpack
    def test_init_root(self, root):
        c = SeqData(root)
        assert c.root.is_root == True
        assert c.nodes == {}

    def test_nodes_chain(self):
        root = RootData(samples, annot)
        c = SeqData(root)

        c.put_data('RC', df4, root)
        node1 = c.get_node_data('RC')
        logdf = np.log1p(node1.X)
        node2 = c.put_data('logRC', logdf, 'RC')

        # chain
        assert root.children == [node1]
        assert node1.parent == root
        assert node1.children == [node2,]
        assert node2.parent == node1
        assert node2.children == []

    def test_seq_data(self):
        root = RootData(samples, annot)
        c = SeqData(root)

        # data: read counts
        c.put_data('RC', df4, root)
        node1 = c.get_node_data('RC')
        assert node1.X.shape == (3, 3)
        df = node1.to_df_samples()
        assert df.shape == (3, 6)
        df = node1.to_df_variables()
        assert df.shape == (7, 3)
        # nodes
        assert set(c.nodes) == {'RC', }
        assert c.data_names() == ['RC']
        # add sample
        sample = pd.Series([3,40], index=['gene1', 'gene3'])
        sample.name = 'sample4'
        node1.put_data(sample)
        # to_df
        df = c.to_df('RC', 0)
        assert df.shape == (4, 6)
        df = c.to_df('RC', 1)
        assert df.shape == (8, 3)

        # statistics: col_stat
        gene_mean = node1.X.apply(np.mean, axis=0)
        gene_mean.name = 'rc_mean'
        node1.col_stat.put('rc_mean', gene_mean)
        df = c.to_df('RC', 1, {'geneID', 'rc_mean'})
        assert df.shape == (6, 3)
        assert set(df) == {'gene1', 'gene2', 'gene3'}
        assert list(df.index) == ['geneID', 'rc_mean', \
            'sample1', 'sample2', 'sample3', 'sample4']

        # statistics: row_stat
        gene_range = node1.X.apply(lambda x: np.max(x) - np.min(x), axis=1)
        gene_range.name = 'rc_range'
        node1.row_stat.put('rc_range', gene_range)
        df = c.to_df('RC', 0, {'age', 'rc_range'})
        assert df.shape == (4, 5)
        assert set(df) == {'age', 'rc_range', 'gene1', 'gene2', 'gene3'}
        assert list(df.index) == ['sample1', 'sample2', 'sample3', 'sample4']

        # log of RC
        logdf = np.log1p(node1.X)
        node2 = c.put_data('logRC', logdf, 'RC')
        assert set(c.nodes) == {'RC', 'logRC'}
        # 
        df = c.to_df('logRC', 0)
        assert df.shape == (4, 6)
        assert set(df) == {'sample_name', 'age', 'gender', \
            'gene1', 'gene2', 'gene3'}
        assert list(df.index) == ['sample1', 'sample2', 'sample3', 'sample4']
        # 
        df = c.to_df('logRC', 1)
        assert df.shape == (8, 3)
        assert set(df) == {'gene1', 'gene2', 'gene3'}
        assert list(df.index) == ['geneID', 'geneName', 'start', 'end', \
            'sample1', 'sample2', 'sample3', 'sample4']

