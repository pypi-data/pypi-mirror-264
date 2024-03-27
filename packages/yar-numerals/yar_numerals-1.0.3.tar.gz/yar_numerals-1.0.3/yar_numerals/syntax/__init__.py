# (c) Copyright by Yar.
#
# Syntactical layer of processing.

from typing import List, Iterable
from ..lexeme import *
from ..grammar import *
from .relation import *

__all__ = [
    "Relation",
    "SyntaxNode",
    "DummySyntaxNode",
]


class SyntaxNode:
    def __init__(self, lexeme: Lexeme) -> None:
        self.lexeme = lexeme
        self.edges: List["SyntaxEdge"] = []

    def add_child(self, lexeme: Lexeme, rel: Relation) -> "SyntaxNode":
        child = SyntaxNode(lexeme)
        return self.add_child_node(child, rel)

    def add_child_node(self, child: "SyntaxNode", rel: Relation) -> "SyntaxNode":
        edge = SyntaxEdge(self, child, rel)
        self.edges.append(edge)
        return child

    def agree(self) -> None:
        for edge in self.edges[::-1]:
            edge.agree()

    def lexemes(self) -> Iterable[Lexeme]:
        yield self.lexeme
        for edge in self.edges:
            yield from edge.child.lexemes()

    def __str__(self):
        return " ".join([l.text() for l in self.lexemes()][::-1])

    def __repr__(self):  # pragma: no cover
        if len(self.edges) == 0:
            return f"SyntaxNode<{repr(self.lexeme)}: []>"
        if len(self.edges) == 1:
            return f"SyntaxNode<{repr(self.lexeme)}: [{repr(self.edges[0])}]>"
        return f"SyntaxNode<{repr(self.lexeme)}: [{len(self.edges)}]>"


class DummySyntaxNode(SyntaxNode):
    def __init__(
        self, form: InflectionForm = None, persistent_form: InflectionForm = None
    ) -> None:
        if persistent_form is None:
            persistent_form = {}
        if form is None:
            form = {}
        super().__init__(DummyLexeme(form, persistent_form))

    def lexemes(self) -> Iterable[Lexeme]:
        for edge in self.edges:
            yield from edge.child.lexemes()


class SyntaxEdge:
    def __init__(self, parent: "SyntaxNode", child: "SyntaxNode", rel: Relation):
        self.parent = parent
        self.child = child
        self.rel = rel

    def agree(self):
        modifier = RelationDef.get(self.rel).modifier(
            self.parent.lexeme, self.child.lexeme
        )
        if modifier:
            self.child.lexeme.form = modifier
        self.child.agree()
        governing = RelationDef.get(self.rel).governing(
            self.child.lexeme, self.parent.lexeme
        )
        if governing:
            self.parent.lexeme.form = governing

    def __repr__(self):  # pragma: no cover
        return f"{self.rel} -> {repr(self.child)}"
