import pytest

from Node import Node
from Lattice import Lattice
from enums import NodeState


@pytest.fixture
def node() -> Node:
    return Node()


@pytest.fixture
def lattice() -> Lattice:
    return Lattice()


class TestNode:
    def test_vacant_state(self, node: Node) -> None:
        assert node.get_state() == NodeState.VACANT

    def test_flip(self, node: Node, lattice: Lattice) -> None:
        node.flip_state(lattice.get_draw_mode())
        assert node.get_state() == NodeState.WALL
