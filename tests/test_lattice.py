import pytest
import random

from enums import DrawMode
from Node import Node
from Lattice import Lattice, LatticeInfo, ScreenDim


@pytest.fixture
def lattice() -> Lattice:
    return Lattice()


class TestLattice:
    def test_initial_state(self, lattice: Lattice) -> None:
        assert type(lattice.get_info()) == LatticeInfo
        assert type(lattice.get_info().screen_dim) == ScreenDim
        assert lattice.get_draw_mode() == DrawMode.WALL

    def test_get_dim(self, lattice: Lattice) -> None:
        dim = lattice.get_dim()
        assert type(dim.nrows) == int
        assert type(dim.ncols) == int

    def test_get_node(self, lattice: Lattice) -> None:
        rand_r = random.randrange(lattice.get_dim().nrows)
        rand_c = random.randrange(lattice.get_dim().ncols)
        assert type(lattice.get_node(rand_r, rand_c)) == Node
    