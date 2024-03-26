from unittest import TestCase
from ddt import ddt, data, unpack
from src.rnaseqdata import StatData

from tests.data.constants import *


@ddt
class TestStatData(TestCase):

    def test_put(self):
        c = StatData()
        c.put('a')
        assert c.data['a'].name == 'a'
        assert c.data['a'].shape == (0,)

        c.put('b', s1)
        assert c.data['b'].shape == (3,)
        assert list(c.data) == ['a', 'b']

        c.put('a', s2)
        assert c.data['a'].shape == (4,)
        assert list(c.data) == ['a', 'b']
    
    @data(
        [None, None, (4, 3), list('ABC'), list('abcd')],
        [None, list('abcf'), (4, 3), list('ABC'), list('abcf')],
        [['A'], list('abc'), (3, 1), ['A'], list('abc')],
        [['A'], list('bca'), (3, 1), ['A'], list('bca')],
        [['A','E'], list('abc'), (3, 2), ['A', 'E'], list('abc')],
        [['B',], None, (4, 1), ['B'], list('bcad')],
    )
    @unpack
    def test_cross_rows(self, stat_names, key1, expect_shape, \
            expect_col, expect_row):
        c = StatData(axis=0)
        c.put('A', s1)
        c.put('B', s2)
        c.put('C')
        res = c.to_df(key1, stat_names)
        assert res.shape == expect_shape
        assert list(res) == expect_col
        assert list(res.index) == expect_row

    @data(
        [None, None, (3, 4), list('abcd'), list('ABC')],
        [None, list('abcf'), (3, 4), list('abcf'), list('ABC')],
        [['A'], list('abc'), (1, 3), list('abc'), ['A']],
        [['A'], list('bca'), (1, 3), list('bca'), ['A']],
        [['A','E'], list('abc'), (2, 3), list('abc'), list('AE')],
        [['B'], None, (1, 4), list('bcad'), ['B']],
    )
    @unpack
    def test_cross_columns(self, stat_names, key1, expect_shape, \
            expect_col, expect_row):
        c = StatData(1)
        c.put('A', s1)
        c.put('B', s2)
        c.put('C')
        res = c.to_df(key1, stat_names)
        assert res.shape == expect_shape
        assert list(res) == expect_col
        assert list(res.index) == expect_row
    
    @data(
        [0, None, None, (0,0)],
        [0, ['sample1'], None, (0,0)],
        [1, None, None, (0,0)],
        [1, ['gene1'], None, (0,0)],
    )
    @unpack
    def test_to_df_empty(self, axis, key1, key2, expect_shape):
        c = StatData(axis)
        res = c.to_df(key1, key2)
        assert res.shape == expect_shape
