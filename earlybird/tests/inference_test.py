
import os
import unittest
import numpy as np
import pathlib
from ..inference import tokenize_sequence, model


class TestInference(unittest.TestCase):

    my_mock_titles = {"title": ["this is a test title",
                                "this is another test title",
                                "omfg more titles",
                                "ugh aren't these titles annoying",
                                "i'm so tired of writing titles"]}

    def test_load_model(self):
        self.assertEqual(
            bool(model), True)

    def test_str_tokenization(self):
        self.assertEqual(type(tokenize_sequence(
            self.my_mock_titles["title"])), np.ndarray)

    def test_strings_padded(self):
        self.assertEqual(len(tokenize_sequence(
            self.my_mock_titles["title"])), 5)

    def test_padding_length(self):
        self.assertEqual(len(tokenize_sequence(
            self.my_mock_titles["title"])[0]), 100)
