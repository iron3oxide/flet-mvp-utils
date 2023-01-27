from dataclasses import asdict
from typing import Protocol

import flet as ft


class DataclassProtocol(Protocol):
    __dataclass_fields__: dict


class MvpView:
    def __init__(self, ref_map: dict[str, ft.Ref]) -> None:
        self.ref_map = ref_map

    def render(self, model: DataclassProtocol):
        model_map = asdict(model)
        for variable_name, ref in self.ref_map.items():
            if model_map[variable_name] == ref.current.value:
                continue
            ref.current.value = model_map[variable_name]
