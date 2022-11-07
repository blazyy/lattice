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
