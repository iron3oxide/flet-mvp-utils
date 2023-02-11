from abstractcp import Abstract, abstract_class_property
from flet_routed_app import RoutedApp
from pydantic import BaseModel, ValidationError

from flet_mvp_utils.error import ErrorMessage
from flet_mvp_utils.observable import Observable


class MvpDataSource(Abstract, Observable):
    current_model = abstract_class_property(BaseModel)

    def __init__(
        self, *, app: RoutedApp | None = None, route_params: dict[str, str]
    ) -> None:
        super().__init__()
        self.model_class = type(self.current_model)
        self.route_params = route_params
        if app:
            self.app = app

    def update_model_partial(self, changes: dict) -> bool:
        model_map = self.current_model.dict()
        for k, v in model_map:
            if changes[k] != v:
                model_map[k] = changes[k]
        return self.update_model_complete(model_map)

    def update_model_complete(self, new_model: dict) -> bool:
        try:
            self.current_model = self.model_class(**new_model)
            return True

        except ValidationError as e:
            modified_model = new_model
            for error in e.errors():
                location = str(error["loc"][0])
                modified_model[location] = ErrorMessage(error["msg"])

            self.current_model = self.model_class(**modified_model)
            return False

        finally:
            self.notify_observers()
