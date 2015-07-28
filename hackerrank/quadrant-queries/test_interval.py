import unittest
from interval import update, Query, intersect_update


class QueryTest(unittest.TestCase):

    def test_case_1(self):
        query_1 = Query(0, 5, 1, 0)
        query_i = Query(2, 3, 0, 1)

        out = update(query_i, [query_1])
        self.assertEquals(out, [Query(0, 1, 1, 0), Query(2, 3, 1, 1), Query(4, 5, 1, 0)])

    def test_case_2(self):
        query_1 = Query(0, 5, 1, 0)
        query_i = Query(2, 3, 1, 0)

        out = update(query_i, [query_1])
        self.assertEquals(out, [Query(0, 1, 1, 0), Query(4, 5, 1, 0)])

    def test_case_3(self):
        query_1 = Query(3, 5, 1, 0)
        query_i = Query(1, 2, 1, 0)

        out = update(query_i, [query_1])
        self.assertEquals(out, [Query(1, 2, 1, 0), Query(3, 5, 1, 0)])

    def test_case_4(self):
        query_1 = Query(3, 5, 1, 0)
        query_2 = Query(6, 7, 1, 0)
        query_i = Query(1, 2, 1, 0)

        out = update(query_i, [query_1, query_2])
        self.assertEquals(out, [Query(1, 2, 1, 0), Query(3, 5, 1, 0), Query(6, 7, 1, 0)])

    def test_case_5(self):
        query_1 = Query(3, 5, 1, 0)
        query_2 = Query(6, 7, 1, 0)
        query_i = Query(8, 9, 1, 0)

        out = update(query_i, [query_1, query_2])
        self.assertEquals(out, [Query(3, 5, 1, 0), Query(6, 7, 1, 0), Query(8, 9, 1, 0)])

    def test_case_6(self):
        query_1 = Query(3, 5, 1, 0)
        query_i = Query(2, 3, 1, 0)

        out = update(query_i, [query_1])
        self.assertEquals(out, [Query(2, 2, 1, 0), Query(4, 5, 1, 0)])

    def test_case_7(self):
        query_1 = Query(3, 5, 1, 0)
        query_i = Query(2, 3, 0, 1)

        out = update(query_i, [query_1])
        self.assertEquals(out, [Query(2, 2, 0, 1), Query(3, 3, 1, 1), Query(4, 5, 1, 0)])

    def test_case_8(self):
        query_1 = Query(3, 5, 1, 0)
        query_i = Query(2, 5, 0, 1)
        out = update(query_i, [query_1])
        self.assertEquals(out, [Query(2, 2, 0, 1), Query(3, 5, 1, 1)])

        query_1 = Query(2, 5, 1, 0)
        query_i = Query(3, 5, 1, 0)
        out = update(query_i, [query_1])
        self.assertEquals(out, [Query(2, 2, 1, 0)])

        query_1 = Query(2, 5, 1, 0)
        query_i = Query(3, 7, 1, 0)
        out = update(query_i, [query_1])
        self.assertEquals(out, [Query(2, 2, 1, 0), Query(6, 7, 1, 0)])

        query_1 = Query(2, 5, 1, 0)
        query_i = Query(3, 7, 0, 1)
        out = update(query_i, [query_1])
        self.assertEquals(out, [Query(2, 2, 1, 0), Query(3,5, 1, 1), Query(6, 7, 0, 1)])

    def test_case_9(self):
        query_1 = Query(2, 5, 1, 0)
        query_i = Query(3, 5, 0, 1)
        out = update(query_i, [query_1])
        self.assertEquals(out, [Query(2, 2, 1, 0), Query(3, 5, 1, 1)])

        query_1 = Query(3, 5, 1, 0)
        query_i = Query(2, 5, 1, 0)
        out = update(query_i, [query_1])
        self.assertEquals(out, [Query(2, 2, 1, 0)])

        query_1 = Query(3, 5, 1, 0)
        query_i = Query(2, 7, 1, 0)
        out = update(query_i, [query_1])
        self.assertEquals(out, [Query(2, 2, 1, 0), Query(6, 7, 1, 0)])

        query_1 = Query(3, 5, 1, 0)
        query_i = Query(2, 7, 0, 1)
        out = update(query_i, [query_1])
        self.assertEquals(out, [Query(2, 2, 0, 1), Query(3,5, 1, 1), Query(6, 7, 0, 1)])

    def test_case_10(self):
        query_1 = Query(3, 5, 1, 0)
        query_i = Query(3, 5, 0, 1)
        out = update(query_i, [query_1])
        self.assertEquals(out, [Query(3, 5, 1, 1)])
        query_1 = Query(3, 5, 1, 0)
        query_i = Query(3, 5, 1, 0)
        out = update(query_i, [query_1])
        self.assertEquals(out, [])

        query_1 = Query(3, 6, 1, 0)
        query_i = Query(3, 5, 1, 0)
        out = update(query_i, [query_1])
        self.assertEquals(out, [Query(6, 6, 1, 0)])

        query_1 = Query(3, 6, 1, 0)
        query_i = Query(3, 5, 0, 1)
        out = update(query_i, [query_1])
        self.assertEquals(out, [Query(3, 5, 1,1), Query(6, 6, 1, 0)])

        query_1 = Query(3, 5, 1, 0)
        query_i = Query(3, 7, 1, 0)
        out = update(query_i, [query_1])
        self.assertEquals(out, [Query(6, 7, 1, 0)])

        query_1 = Query(3, 5, 1, 0)
        query_i = Query(3, 7, 0, 1)
        out = update(query_i, [query_1])
        self.assertEquals(out, [Query(3, 5, 1, 1), Query(6, 7, 0, 1)])


class IntersectUpdateTest(unittest.TestCase):

    def test_corner_cases(self):

        query_1 = Query(0,2,1,0)
        query_2 = Query(3,5,0,1)
        query_i = Query(1,2,None, None)
        out, query = intersect_update(query_i, [query_1, query_2])
        self.assertEquals(out, [Query(0,0,1,0), Query(3,5,0,1)])
        self.assertEquals(query, [Query(1,2, 1,0)])

        out, query = intersect_update(query_i, [query_2])
        self.assertEquals(out, [Query(3,5,0,1)])
        self.assertEquals(query, [])
        query_1 = Query(-1,0,1,0)
        out, query = intersect_update(query_i, [query_1])
        self.assertEquals(out, [Query(-1,0,1,0)])
        self.assertEquals(query, [])

    def test_item_init_less_interval_init(self):
        query_1 = Query(0,4,1,0)
        query_i = Query(1,2,None, None)
        out, query = intersect_update(query_i, [query_1])
        self.assertEquals(out, [Query(0,0,1,0), Query(3,4,1,0)]) 
        self.assertEquals(query, [Query(1,2,1,0)])

        query_1 = Query(0,4,1,0)
        query_i = Query(1,4,None, None)
        out, query = intersect_update(query_i, [query_1])
        self.assertEquals(out, [Query(0,0,1,0)])
        self.assertEquals(query, [Query(1,4,1,0)])

        query_1 = Query(0,4,1,0)
        query_i = Query(1,6,None, None)
        out, query = intersect_update(query_i, [query_1])
        self.assertEquals(out, [Query(0,0,1,0)])
        self.assertEquals(query, [Query(1,4,1,0)])

    def test_item_init_gt_interval_init(self):
        query_1 = Query(2,4,1,0)
        query_i = Query(1,2,None, None)
        out, query = intersect_update(query_i, [query_1])
        self.assertEquals(out, [Query(3,4,1,0)]) 
        self.assertEquals(query, [Query(2,2,1,0)])

        query_1 = Query(2,4,1,0)
        query_i = Query(1,4,None, None)
        out, query = intersect_update(query_i, [query_1])
        self.assertEquals(out, [])
        self.assertEquals(query, [Query(2,4,1,0)])

        query_1 = Query(2,4,1,0)
        query_i = Query(1,6,None, None)
        out, query = intersect_update(query_i, [query_1])
        self.assertEquals(out, [])
        self.assertEquals(query, [Query(2,4,1,0)])
    
    def test_item_init_eq_interval_init(self):
        query_1 = Query(1,4,1,0)
        query_i = Query(1,2,None, None)
        out, query = intersect_update(query_i, [query_1])
        self.assertEquals(out, [Query(3,4,1,0)]) 
        self.assertEquals(query, [Query(1,2,1,0)])

        query_1 = Query(1,4,1,0)
        query_i = Query(1,4,None, None)
        out, query = intersect_update(query_i, [query_1])
        self.assertEquals(out, [])
        self.assertEquals(query, [Query(1,4,1,0)])

        query_1 = Query(1,4,1,0)
        query_i = Query(1,6,None, None)
        out, query = intersect_update(query_i, [query_1])
        self.assertEquals(out, [])
        self.assertEquals(query, [Query(1,4,1,0)])


if __name__ == '__main__':
    unittest.main()
