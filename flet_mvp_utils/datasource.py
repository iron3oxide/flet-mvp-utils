from typing import Any, Type

from pydantic import BaseModel, ValidationError

from flet_mvp_utils.error import ErrorMessage
from flet_mvp_utils.observable import Observable


class MvpDataSource(Observable):
    def __init__(self, model_class: Type[BaseModel]) -> None:
        super().__init__()
        self.model_class = model_class
        self.current_model: Any = model_class()

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
