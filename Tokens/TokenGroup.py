
from Tokens.Token import TokenType

class TokenGroup:

    def group_tokens(self, tokens, index):
        tokens_list = []
        while index < len(tokens) and tokens[index].token_type not in (TokenType.OPERATION, TokenType.BRACKET):
            tokens_list.append(tokens[index])
            index += 1
        return tokens_list

    def create_tokens(self, tokens):
        index = 0
        tokens_grouped = []
        while index < len(tokens):
            if tokens[index].token_type in (TokenType.BRACKET, TokenType.OPERATION):
                tokens_grouped.append([tokens[index]])
                index += 1
            else:
                tokens_list = self.group_tokens(tokens, index)
                tokens_grouped.append(tokens_list)
                index += len(tokens_list)
        return tokens_grouped

