import pytest

from enums import DrawMode
from Lattice import Lattice, LatticeInfo, ScreenDim


@pytest.fixture
def lattice() -> Lattice:
    return Lattice()


class TestLattice:
    def test_lattice_initial_state(self, lattice: Lattice) -> None:
        assert type(lattice.get_info()) == LatticeInfo
        assert type(lattice.get_info().screen_dim) == ScreenDim
        assert lattice.get_draw_mode() == DrawMode.WALL
