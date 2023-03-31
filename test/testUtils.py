
from collections import namedtuple


TokenTest = namedtuple('TokenTest', 'type data', defaults=[0])


def check_tokens(tokens, tokens_test):
    assert len(tokens) == len(tokens_test)
    for token, token_test in zip(tokens, tokens_test):
        assert token.type == token_test.type
        assert token.data == token_test.data


