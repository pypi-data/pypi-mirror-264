import os
from unittest import TestCase

from src.rnaseqdata import AnnotData
from tests import DATA_DIR

class TestAnnotations(TestCase):

    def test_build_annotations(self):
        c = AnnotData(1)

        infile = os.path.join(DATA_DIR, 'Homo_sapiens_mature.json')
        c.from_json(infile)
        assert len(c.data) == 2656
        assert c.data['hsa-let-7b-3p'] == {'ID': 'hsa-let-7b-3p', \
            'database': 'miRBase', 'annot_type': 'miRNA_mature', \
            'accession': 'MIMAT0004482', 'organism_name': 'Homo sapiens', \
            'specie_name': 'Homo_sapiens'}

        # omit duplicates
        c.from_json(infile)
        assert len(c.data) == 2656

        # additional annotations
        infile = os.path.join(DATA_DIR, 'Homo_sapiens_hairpin.json')
        c.from_json(infile)
        assert len(c.data) == 4573
        c.data['hsa-let-7c'] == {'ID': 'hsa-let-7c', 'database': 'miRBase', \
            'annot_type': 'miRNA_hairpin', 'accession': 'MI0000064', \
            'organism_name': 'Homo sapiens', 'specie_name': 'Homo_sapiens'}

        # to data frame
        df = c.to_df()
        assert df.shape == (6, 4573)
        df = c.to_df(None, ['ID', 'accession'])
        assert df.shape == (2, 4573)
        names = ["hsa-let-7b-3p", 'hsa-let-7c',]
        df = c.to_df(names, ['ID', 'accession'])
        assert df.shape == (2, 2)
