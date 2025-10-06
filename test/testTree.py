
from unittest import TestCase

from utils import check_tree
from tokens.parser import Parser

from postfix.tree import create_tree
from postfix.postfix import Postfix


class TestTree(TestCase):

    def test_tree_1(self):
        tokens = Parser("(2 + x)(x - 4)").parse()
        postfix = Postfix().create_postfix(tokens)
        root = create_tree(postfix)
        check_tree(root, postfix)


    def test_tree_2(self):
        tokens = Parser("10tgx - xctgx").parse()
        postfix = Postfix().create_postfix(tokens)
        root = create_tree(postfix)
        check_tree(root, postfix)
