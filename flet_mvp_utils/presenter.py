from flet_mvp_utils.datasource import MvpDataSource
from flet_mvp_utils.protocols import MvpViewProtocol


class MvpPresenter:
    def __init__(self, data_source: MvpDataSource, view: MvpViewProtocol) -> None:
        self.data_source = data_source
        self.view = view
        self.data_source.register(self.update_view)

    def build(self) -> None:
        self.view.build(self)

    def update_view(self) -> None:
        self.view.render(self.data_source.current_model)
