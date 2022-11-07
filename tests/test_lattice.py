import pytest
import random

from Node import Node
from enums import DrawMode, NodeState
from Lattice import Lattice, LatticeInfo, ScreenDim, draw_mode_to_node_state_mapping


@pytest.fixture
def lattice() -> Lattice:
    return Lattice()


class TestLattice:
    def test_initial_state(self, lattice: Lattice) -> None:
        assert type(lattice.get_info()) == LatticeInfo
        assert type(lattice.get_info().screen_dim) == ScreenDim
        assert lattice.get_draw_mode() == DrawMode.SET_WALL

    def test_get_info(self, lattice: Lattice) -> None:
        assert type(lattice.get_info()) == LatticeInfo

    def test_get_dim(self, lattice: Lattice) -> None:
        dim = lattice.get_dim()
        assert type(dim.nrows) == int
        assert type(dim.ncols) == int

    def test_get_draw_mode(self, lattice: Lattice) -> None:
        assert type(lattice.get_draw_mode()) == DrawMode

    def test_set_draw_mode(self, lattice: Lattice) -> None:
        random_draw_mode = random.choice([draw_mode for draw_mode in DrawMode])
        lattice.set_draw_mode(random_draw_mode)
        assert type(lattice.get_draw_mode()) == DrawMode
        assert lattice.get_draw_mode() == random_draw_mode

    def test_randomize(self, lattice: Lattice) -> None:
        lattice.randomize()
        nrows, ncols = lattice.get_dim()
        for r in range(nrows):
            for c in range(ncols):
                node = lattice.get_node(r, c)
                assert type(node) == Node
                assert node.get_state() in [NodeState.VACANT, NodeState.WALL]


    def test_get_node(self, lattice: Lattice) -> None:
        rand_r = random.randrange(lattice.get_dim().nrows)
        rand_c = random.randrange(lattice.get_dim().ncols)
        assert type(lattice.get_node(rand_r, rand_c)) == Node

    def test_change_node_state(self, lattice: Lattice) -> None:
        for draw_mode in DrawMode:
            lattice.set_draw_mode(draw_mode)
            lattice.change_node_state(0, 0)
            lattice.get_node(0, 0).get_state() == draw_mode_to_node_state_mapping[draw_mode]
            
    