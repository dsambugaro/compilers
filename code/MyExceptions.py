
class Error(Exception):
    pass

class PruningError(Exception):
    pass

class SemanticError(Exception):
    pass

class CommentInvalidSyntax(SyntaxError):
    pass

class IllegalCharacter(SyntaxError):
    pass
