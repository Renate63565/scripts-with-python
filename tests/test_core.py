import unittest

from scripts_with_python.core import Bag
from scripts_with_python import Bag as ReExportedBag


class TestInsert(unittest.TestCase):

    def test_single_insert(self):
        b = Bag()
        b.insert("a")
        self.assertEqual(b.count("a"), 1)

    def test_multiple_inserts_accumulate(self):
        b = Bag()
        b.insert("a")
        b.insert("a")
        b.insert("a")
        self.assertEqual(b.count("a"), 3)

    def test_insert_with_times(self):
        b = Bag()
        b.insert("a", 5)
        self.assertEqual(b.count("a"), 5)

    def test_insert_zero_is_noop(self):
        b = Bag(["a"])
        b.insert("a", 0)
        self.assertEqual(b.count("a"), 1)
        b.insert("b", 0)
        self.assertEqual(b.count("b"), 0)

    def test_insert_negative_raises(self):
        b = Bag()
        with self.assertRaises(ValueError):
            b.insert("a", -1)

    def test_insert_bool_rejected(self):
        """bool is a subclass of int but must be refused as an uncountable."""
        b = Bag()
        with self.assertRaises(TypeError):
            b.insert("a", True)


class TestRemove(unittest.TestCase):

    def test_remove_single(self):
        b = Bag(["a", "a", "a"])
        b.remove("a")
        self.assertEqual(b.count("a"), 2)

    def test_remove_all_deletes_key(self):
        b = Bag(["a", "a"])
        b.remove("a", 2)
        self.assertEqual(b.count("a"), 0)
        self.assertNotIn("a", b)

    def test_remove_too_many_raises(self):
        b = Bag(["a"])
        with self.assertRaises(ValueError):
            b.remove("a", 2)

    def test_remove_absent_raises(self):
        b = Bag()
        with self.assertRaises(ValueError):
            b.remove("ghost")

    def test_remove_zero_is_noop(self):
        b = Bag(["a", "a"])
        b.remove("a", 0)
        self.assertEqual(b.count("a"), 2)

    def test_remove_negative_raises(self):
        b = Bag(["a"])
        with self.assertRaises(ValueError):
            b.remove("a", -1)

    def test_remove_bool_rejected(self):
        b = Bag(["a"])
        with self.assertRaises(TypeError):
            b.remove("a", False)


class TestCount(unittest.TestCase):

    def test_count_absent_is_zero(self):
        b = Bag()
        self.assertEqual(b.count("nothing"), 0)

    def test_count_after_partial_remove(self):
        b = Bag(["x", "x", "x"])
        b.remove("x", 2)
        self.assertEqual(b.count("x"), 1)


class TestIterationAndLen(unittest.TestCase):

    def test_len_counts_multiplicity(self):
        b = Bag(["a", "a", "b"])
        self.assertEqual(len(b), 3)

    def test_iter_yields_each_copy(self):
        b = Bag(["a", "a", "b"])
        yielded = sorted(b)
        self.assertEqual(yielded, ["a", "a", "b"])

    def test_iter_empty(self):
        b = Bag()
        self.assertEqual(list(b), [])


class TestEquality(unittest.TestCase):

    def test_equal_bags(self):
        self.assertEqual(Bag(["a", "b", "a"]), Bag(["a", "a", "b"]))

    def test_unequal_multiplicity(self):
        self.assertNotEqual(Bag(["a", "a"]), Bag(["a"]))

    def test_unequal_keys(self):
        self.assertNotEqual(Bag(["a"]), Bag(["b"]))

    def test_eq_with_non_bag(self):
        self.assertNotEqual(Bag(["a"]), {"a": 1})


class TestConstructor(unittest.TestCase):

    def test_from_iterable(self):
        b = Bag([1, 2, 1, 3, 1])
        self.assertEqual(b.count(1), 3)
        self.assertEqual(b.count(2), 1)
        self.assertEqual(b.count(3), 1)

    def test_empty_default(self):
        b = Bag()
        self.assertEqual(len(b), 0)
        self.assertEqual(list(b), [])

    def test_from_generator(self):
        b = Bag(x for x in ["a", "a", "b"])
        self.assertEqual(b.count("a"), 2)
        self.assertEqual(b.count("b"), 1)


class TestUnhashable(unittest.TestCase):

    def test_insert_unhashable_raises(self):
        b = Bag()
        with self.assertRaises(TypeError):
            b.insert([1, 2])

    def test_constructor_with_unhashable_raises(self):
        with self.assertRaises(TypeError):
            Bag([[1]])


class TestReExport(unittest.TestCase):

    def test_top_level_is_same_class(self):
        self.assertIs(Bag, ReExportedBag)


if __name__ == "__main__":
    unittest.main()
