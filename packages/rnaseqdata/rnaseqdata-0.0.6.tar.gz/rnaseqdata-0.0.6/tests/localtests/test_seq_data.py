import os
from unittest import TestCase

from src.rnaseqdata import load_seqdata, dump_seqdata, NodeData
from tests.data.constants import df4, annot, samples
from tests import DATA_DIR, TMP_DIR


class TestSeqData(TestCase):
    def setUp(self):
        self.file = os.path.join(TMP_DIR, 'test.obj')

    def tearDown(self):
        try:
            os.remove(self.file)
        except Exception as e:
            pass
    
    def test_iterative(self):
        seqdata = load_seqdata(self.file)
        rc_node = NodeData(seqdata.root, 'RC')