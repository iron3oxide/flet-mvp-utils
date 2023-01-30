from typing import List, Optional

import flet as ft
from pydantic import BaseModel

from flet_mvp_utils.error import ErrorMessage


class MvpView(ft.View):
    def __init__(
        self,
        ref_map: dict[str, ft.Ref],
        *,
        route: Optional[str] = None,
        controls: Optional[List[ft.Control]] = None,
        appbar: Optional[ft.AppBar] = None,
        floating_action_button: Optional[ft.FloatingActionButton] = None,
        navigation_bar: Optional[ft.NavigationBar] = None,
        vertical_alignment: ft.MainAxisAlignment = ft.MainAxisAlignment.NONE,
        horizontal_alignment: ft.CrossAxisAlignment = ft.CrossAxisAlignment.NONE,
        spacing: ft.OptionalNumber = None,
        padding: ft.PaddingValue = None,
        bgcolor: Optional[str] = None,
        scroll: Optional[ft.ScrollMode] = None,
        auto_scroll: Optional[bool] = None,
    ) -> None:
        super().__init__(
            route,
            controls,
            appbar,
            floating_action_button,
            navigation_bar,
            vertical_alignment,
            horizontal_alignment,
            spacing,
            padding,
            bgcolor,
            scroll,
            auto_scroll,
        )

        self.ref_map = ref_map

    def render(self, model: BaseModel) -> None:
        model_map = model.dict()
        for variable_name, ref in self.ref_map.items():
            control_attribute_name = "value"
            if not hasattr(ref.current, control_attribute_name):
                control_attribute_name = "text"
            if isinstance(model_map[variable_name], ErrorMessage):
                control_attribute_name = "error_text"

            control_attribute_value = getattr(ref.current, control_attribute_name)

            if model_map[variable_name] == control_attribute_value:
                continue
            setattr(ref.current, control_attribute_name, model_map[variable_name])
