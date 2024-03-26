import os
from unittest import TestCase

from src.rnaseqdata import load_seqdata, dump_seqdata
from tests.data.constants import df4, annot, samples
from tests import DATA_DIR, TMP_DIR

class TestStore(TestCase):
    def setUp(self):
        self.file = os.path.join(TMP_DIR, 'test.obj')

    def tearDown(self):
        try:
            os.remove(self.file)
        except Exception as e:
            pass

    def test_empty(self):
        seqdata = load_seqdata(self.file)
        assert seqdata.data_names() == []
        assert seqdata.to_df('RC') is None

        res = dump_seqdata(seqdata, self.file)
        assert res == True
        assert os.path.isfile(self.file) == True

        seqdata = load_seqdata(self.file)
        assert seqdata.data_names() == []
        assert seqdata.to_df('RC') is None

    def test_demo(self):
        seqdata = load_seqdata(self.file)
        assert seqdata.data_names() == []
        assert seqdata.to_df('RC') is None

        # addd data
        seqdata.put_samples(samples)
        seqdata.put_variables(annot)
        seqdata.put_data('RC', df4)
        assert seqdata.data_names() == ['RC',]
        assert seqdata.to_df('RC', 0).shape == (3, 6)
        assert seqdata.to_df('RC', 1).shape == (7, 3)

        res = dump_seqdata(seqdata, self.file)
        assert res == True
        assert os.path.isfile(self.file) == True
        seqdata = load_seqdata(self.file)
        assert seqdata.data_names() == ['RC',]
        assert seqdata.to_df('RC', 0).shape == (3, 6)
        assert seqdata.to_df('RC', 1).shape == (7, 3)

    def test_annotations(self):
        seqdata = load_seqdata(self.file)
        df = seqdata.root.samples.to_df()
        assert df.shape == (0, 0)
        df = seqdata.root.variables.to_df()
        assert df.shape == (0, 0)

        infile = os.path.join(DATA_DIR, 'Homo_sapiens_mature.json')
        seqdata.put_variables(infile)
        df = seqdata.root.samples.to_df()
        assert df.shape == (0, 0)
        df = seqdata.root.variables.to_df()
        assert df.shape == (6, 2656)

        infile = os.path.join(DATA_DIR, 'Homo_sapiens_hairpin.json')
        seqdata.put_variables(infile)
        df = seqdata.root.samples.to_df()
        assert df.shape == (0, 0)
        df = seqdata.root.variables.to_df()
        assert df.shape == (6, 4573)

        res = dump_seqdata(seqdata, self.file)
        assert res == True
        seqdata = load_seqdata(self.file)
        df = seqdata.root.samples.to_df()
        assert df.shape == (0, 0)
        df = seqdata.root.variables.to_df()
        assert df.shape == (6, 4573)
