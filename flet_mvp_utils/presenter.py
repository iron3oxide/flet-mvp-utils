from dataclasses import dataclass

from flet_mvp_utils.datasource import MvpDataSource
from flet_mvp_utils.model import MvpModel
from flet_mvp_utils.protocols import MvpPresenterProtocol, MvpViewProtocol
from flet_mvp_utils.view import MvpView


@dataclass
class MvpPresenter:
    data_source: MvpDataSource
    view: MvpViewProtocol

    def __post_init__(self) -> None:
        self.data_source.register(self.update_view)

    def build(self) -> None:
        self.view.build(self)

    def update_view(self) -> None:
        self.view.render(self.data_source.current_model)


class MockM(MvpModel):
    age: int = 0


class MockDS(MvpDataSource):
    current_model = MockM()

    def mock(self):
        print(self.current_model.age)


class MockV(MvpView):
    ref_map = {}

    def build(self, presenter: MvpPresenterProtocol) -> None:
        ...


@dataclass
class MockP(MvpPresenter):
    data_source: MockDS
    view: MockV

    def test(self):
        self.data_source.mock()


m = MockDS(route_params={})
v = MockV()
p = MockP(m, v)
p.test()
