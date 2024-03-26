from unittest import TestCase
from ddt import ddt, data, unpack

from src.rnaseqdata import RootData, NodeData
from tests.data.constants import *


@ddt
class TestNodeData(TestCase):

    @data(
        ['new', 'new'],
        [None, 'default'],
    )
    @unpack
    def test_name(self, name, expect):
        c = NodeData(RootData(), name)
        assert c.name == expect

    @data(
        [None, (0, 0)],
        [df1, (3, 3)],
        [s1, (3,1)],
        [l1, (3,1)],
    )
    @unpack
    def test_X(self, X, expect_shape):
        c = NodeData(RootData(), 'test', X)
        assert c.X.shape == expect_shape

    def test_nodes_tree(self):
        root = RootData()

        c1 = NodeData(root, 'test1', df1)
        assert c1.parent == root
        assert root.children == [c1,]

        c2 = NodeData(root, 'test2', df2)
        assert c2.parent == root
        assert root.children == [c1, c2]

        c3 = NodeData(c1, 'test3', df2)
        assert c3.parent == c1
        assert c1.children == [c3,]
        assert root.children == [c1, c2]

    def test_default_node(self):
        c = NodeData(RootData(), 'test', df4)

        # row names and column names
        assert c.name == 'test'
        assert c.X.shape == (3,3)
        assert list(c.X.index) == ['sample1', 'sample2', 'sample3']
        assert list(c.X) == ['gene1', 'gene2', 'gene3']

        res = c.row_labels()
        assert list(res) == []
        assert list(res.index) == ['sample1', 'sample2', 'sample3']

        res = c.col_labels()
        assert list(res) == ['gene1', 'gene2', 'gene3']
        assert list(res.index) == []

    @data(
        [
            pd.Series(None, name='s1'),
            pd.Series([1,2], index=list('ab'), name='s2'),
            pd.Series([1,2], index=list('ab'), name='s1'),
        ],
        [
            pd.Series([1,2], index=list('ab'), name='s1'),
            pd.Series(None, name='s2'),
            pd.Series([1,2], index=list('ab'), name='s1'),
        ],
        [
            pd.Series(None, name='s1'),
            pd.Series(None, name='s2'),
            pd.Series(None, name='s1'),
        ],
        [
            pd.Series([1,2], index=list('ab'), name='s1'),
            pd.Series([1,3], index=list('ac'), name='s2'),
            pd.Series([2,2,3], index=list('abc'), name='s1'),
        ],
        [
            pd.Series([2,4], index=list('bd'), name='s1'),
            pd.Series([3,1], index=list('ca'), name='s2'),
            pd.Series([1,2,3,4], index=list('abcd'), name='s1'),
        ],
    )
    @unpack
    def test_combine_series(self, s1, s2, expect):
        res = NodeData.combine_series(s1,s2)
        assert res.equals(expect) == True


    def test_put_data(self):
        c = NodeData(RootData(), 'test', df4)

        s = pd.Series([0, 10, 212], index=['gene3', 'gene1', 'gene2'], name='sample4')
        c.put_data(s)
        assert list(c.X)== ['gene1', 'gene2', 'gene3']
        assert list(c.X.loc['sample1']) == list(df4.loc['sample1'])
        assert list(c.X.loc['sample4']) == [10., 212., 0.]

        # different columns
        s = pd.Series([10, 21, 2], index=['gene4', 'gene1', 'gene2'], name='sample5')
        c.put_data(s)
        assert list(c.X)== ['gene1', 'gene2', 'gene3', 'gene4']
        assert list(c.X.loc['sample1']) == [23., 10., 0., 0.]
        assert list(c.X.loc['sample5']) == [21., 2., 0., 10.]

    def test_update_node(self):
        '''
        update X with identical name
        '''
        c = NodeData(RootData(), 'test', df4)
        
        # new row
        s = pd.Series([10, 21, 2], index=['gene4', 'gene1', 'gene2'], name='sample5')
        c.put_data(s)
        assert list(c.X) == ['gene1', 'gene2', 'gene3', 'gene4']
        assert list(c.X.loc['sample5']) == [21.0, 2.0, .0, 10.0]
        assert list(c.X.loc['sample1']) == [23.0, 10.0, .0, .0]

        # update values: add values
        s = pd.Series([10, 20], index=['gene1', 'gene2'], name='sample5')
        c.put_data(s)
        assert list(c.X) == ['gene1', 'gene2', 'gene3', 'gene4']
        assert list(c.X.loc['sample5']) == [31., 22., .0, 10.]
        assert list(c.X.loc['sample1']) == [23.0, 10.0, .0, .0]

        # add new row
        s = pd.Series([30, 10], index=['gene5', 'gene1'], name='sample5')
        res = c.put_data(s)
        assert list(c.X) == ['gene1', 'gene2', 'gene3', 'gene4', 'gene5']
        assert list(c.X.loc['sample5']) == [41.0, 22.0, .0, 10.0, 30.0]
        assert list(c.X.loc['sample1']) == [23.0, 10.0, .0, .0, .0]

    def test_put_data_duplicate(self):
        c = NodeData(RootData(), 'test')
        s = pd.Series([0,1,2,3,4], index=list('cabba'), name='s1')
        c.put_data(s)
        assert list(c.X) == list('abc')
        assert list(c.X.index) == ['s1',]
        assert list(c.X.loc['s1']) == [1.0, 2.0, .0]

        s = pd.Series([1,2,3], index=list('..a'), name='s2')
        c.put_data(s)
        assert list(c.X) == list('abc.')
        assert list(c.X.index) == ['s1', 's2']
        assert list(c.X.loc['s1']) == [1.0, 2.0, .0, .0]
        assert list(c.X.loc['s2']) == [3.0, .0, .0, 1.0]

    def test_duplicate_col(self):
        '''
        later override the previous
        '''
        c = NodeData(RootData(), 'test', df_dup1)
        assert set(c.X) == {'gene1', 'gene2'}
        assert list(c.X['gene2']) == [0., 10., 78.] 

    def test_duplicate_index(self):
        c = NodeData(RootData(), 'test', df_dup2)
        assert list(c.X['gene1']) == [23.0, 10.0, .0, .0]
        assert list(c.X['gene2']) == [10.0, 120.0, .0, .0]
        assert list(c.X['gene3']) == [.0, 10.0, 78.0, .0]

    def test_sort(self):
        c = NodeData(RootData(), 'test', df_dup2)
        assert list(df_dup2) == ['gene3', 'gene1', 'gene2']
        assert list(c.X) == ['gene1', 'gene2', 'gene3']
        assert list(c.X.index) == ['sample1', 'sample2', 'sample3', 'sample4']

    def test_X_in_matrx(self):
        '''
        not index/column names are defined
        '''
        c = NodeData(RootData(), 'test', np.eye(3))
        assert list(c.X) == [0, 1, 2]
        assert list(c.X.index) == [0, 1, 2]

    def test_X_data_type(self):
        '''
        different data type
        '''
        c = NodeData(RootData(), 'test', df_wrong)
        res = c.X.map(type)
        assert res.all()['age'] == True
        assert res.all()['gender'] == True

    def test_load_X(self):
        '''
        load X in loop
        '''
        c = NodeData(RootData(), 'test')
        for s in (s1, s2, pd.Series(None)):
            c.put_data(s)
        assert c.X.shape == (3, 4)
        assert list(c.X) == list('abcd')
        assert list(c.X.index) == [1, 2, 3]

    def test_labels_1(self):
        '''
        root data is empty
        '''
        c = NodeData(RootData(), 'test', df4)

        # add row/column
        s = pd.Series([10, 21, 2], index=['gene4', 'gene1', 'gene2'])
        c.put_data(s)
        labels = c.row_labels()
        assert list(labels) == []
        assert list(labels.index) == ['sample1', 'sample2', 'sample3', 4]

        # missing data
        s = pd.Series(None, index=['gene1', 'gene2'])
        c.put_data(s)
        labels = c.row_labels()
        assert list(labels) == []
        assert list(labels.index) == ['sample1', 'sample2', 'sample3', 4, 5]

    @data(
        [
            None, (4, 3),
            {'sample_name', 'age', 'gender'},
        ],
        [
            {'sample_name', 'age', 'gender'}, (4, 3),
            {'sample_name', 'age', 'gender'},
        ],
        [
            {'gender', 'XX',}, (4, 2),
            {'gender', 'XX',},
        ],
    )
    @unpack
    def test_labels_2(self, labels, expect_shape, expect_col):
        '''
        sample info and annotations
        '''
        c = NodeData(RootData(samples, annot), 'test', df4)
        s = pd.Series([10, 21, 2], index=['gene4', 'gene1', 'gene2'], name='sample4')
        c.put_data(s)

        df = c.row_labels(labels)
        assert df.shape == expect_shape
        assert set(df) == expect_col
        assert list(df.index) == ['sample1', 'sample2', 'sample3', 'sample4']

    @data(
        [
            RootData(), None, (3, 3),
            {'gene1','gene2','gene3',},
            {'sample1','sample2','sample3'},
        ],
        [
            RootData(samples, annot), None, (3, 6),
            {'sample_name', 'age', 'gender', 'gene1','gene2','gene3',},
            {'sample1','sample2','sample3'},
        ],
        [
            RootData(samples, annot), {'gender', 'age',},
            (3, 5),
            {'gender', 'age', 'gene1','gene2','gene3',},
            {'sample1','sample2','sample3'},
        ],
        [
            RootData(samples, annot), {'gender', 'XX'},
            (3, 5),
            {'gender', 'XX', 'gene1','gene2','gene3',},
            {'sample1','sample2','sample3'},
        ],
    )
    @unpack
    def test_to_df_samples(self, parent, labels, \
            expect_shape, expect_col, expect_row):
        c = NodeData(parent, 'test', df4)
        df = c.to_df_samples(labels)
        assert df.shape == expect_shape
        assert set(df) == expect_col
        assert set(df.index) == expect_row

    @data(
        [
            RootData(), None,
            (3, 3), {'gene1','gene2','gene3',},
            {'sample1','sample2','sample3'},
        ],
        [
            RootData(samples, annot), None,
            (7, 3), {'gene1','gene2','gene3',},
            {'geneID', 'geneName', 'start', 'end', \
                'sample1','sample2','sample3'},
        ],
        [
            RootData(samples, annot), {'geneID', 'start'},
            (5, 3), {'gene1','gene2','gene3',},
            {'geneID', 'start', 'sample1','sample2','sample3'},
        ],
        [
            RootData(samples, annot), {'geneID', 'XX'},
            (5, 3), {'gene1','gene2','gene3',},
            {'geneID', 'XX', 'sample1','sample2','sample3'},
        ],
    )
    @unpack
    def test_to_df_variables(self, parent, labels, \
            expect_shape, expect_col, expect_row):
        c = NodeData(parent, 'test', df4)
        df = c.to_df_variables(labels)
        assert df.shape == expect_shape
        assert set(df) == expect_col
        assert set(df.index) == expect_row

    def test_col_stat(self):
        root = RootData(samples, annot)
        c = NodeData(root, 'RC', df4)
        # add stat data
        rc_range = c.X.apply(lambda x: np.max(x)-np.min(x), axis=0)
        c.col_stat.put('rc_range', rc_range)
        rc_mean = c.X.apply(np.mean, axis=0)
        c.col_stat.put('rc_mean', rc_mean)
        
        # test to_df()
        df = c.col_stat.to_df()
        assert df.shape == (2, 3)
        assert list(c.col_stat.data) == ['rc_range', 'rc_mean']
        
        # test col_labels()
        df = c.col_labels()
        assert df.shape == (6, 3)
        assert list(df.index) == ['geneID', 'geneName', 'start', \
            'end', 'rc_range', 'rc_mean']
        assert list(df) == ['gene1', 'gene2', 'gene3']

        df = c.col_labels({'geneName', 'rc_range'})
        assert df.shape == (2, 3)
        assert set(df.index) == {'geneName', 'rc_range'}
        assert set(df) == {'gene1', 'gene2', 'gene3'}

        df = c.col_labels({'geneName', 'xx', 'rc_range'})
        assert df.shape == (3, 3)
        assert set(df.index) == {'xx', 'geneName', 'rc_range'}
        assert set(df) == {'gene1', 'gene2', 'gene3'}

    def test_row_stat(self):
        root = RootData(samples, annot)
        c = NodeData(root, 'RC', df4)
        # add stat data
        gene_max = c.X.apply(np.max, axis=1)
        c.row_stat.put('gene_max', gene_max)
        assert list(c.row_stat.data) == ['gene_max']
        
        # test to_df()
        df = c.row_stat.to_df()
        assert df.shape == (3, 1)
        assert list(df) == ['gene_max']
        assert list(df.index) == ['sample1', 'sample2', 'sample3']

        # test row_labels()
        df = c.row_labels()
        assert df.shape == (3, 4)
        assert list(df) == ['sample_name', 'age', 'gender', 'gene_max']
        assert list(df.index) == ['sample1', 'sample2', 'sample3']

        df = c.row_labels({'age', 'gene_max',})
        assert df.shape == (3, 2)
        assert set(df) == {'age', 'gene_max'}
        assert set(df.index) == {'sample1', 'sample2', 'sample3'}

        df = c.row_labels({'xx', 'age', 'gene_max',})
        assert df.shape == (3, 3)
        assert set(df) == {'age', 'xx', 'gene_max'}
        assert set(df.index) == {'sample1', 'sample2', 'sample3'}
