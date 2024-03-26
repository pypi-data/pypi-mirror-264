from unittest import TestCase
from src.rnaseqdata import RandomData


class TestRandomData(TestCase):

    def test_norm_X(self):
        res = RandomData(100, 2000).norm_X()
        assert res.shape == (100, 2000)
    
    def test_sample_info(self):
        res = RandomData(100,200).sample_info()
        assert list(res) == ['sample_name', 'age', 'gender', 'level']

    def test_gene_annot(self):
        res = RandomData(100,200).gene_annot()
        assert list(res) == ['gene_name', 'start',]
    
    def test_normal_seqdata(self):
        res = RandomData(100,200).normal_seqdata()
        assert res.root.samples.to_df().shape == (4, 100)
        assert res.root.variables.to_df().shape == (200, 2)
        assert res.to_df('normRC').shape == (100, 200)