import pytest

from Node import Node
from Lattice import Lattice
from enums import NodeState


@pytest.fixture
def node():
    return Node()

@pytest.fixture
def lattice():
  return Lattice()


class TestNode:
    def test_vacant_state(self, node: Node):
        assert node.get_state() == NodeState.VACANT

    def test_flip(self, node: Node, lattice: Lattice):
      node.flip_state(lattice.get_draw_mode())
      assert node.get_state() == NodeState.WALL
