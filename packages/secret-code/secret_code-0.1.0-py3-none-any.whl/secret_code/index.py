from typing import Callable, List
from nicegui import ui

from secret_code.core import need_show_pwd, load_ui, enter_password, get_secret_codes


class PwdDialog(ui.dialog):
    def __init__(self) -> None:
        super().__init__(value=False)

        self._on_pwd_entereds: List[Callable[[], None]] = []

        self.props("persistent")

        with self, ui.card():
            with ui.card_section():
                self._input_pwd = ui.input("输入文章密码").on(
                    "keyup.enter", self.check_password
                )

            with ui.card_actions():
                ui.button("确定", on_click=self.check_password).props("dense")
                ui.button("取消", on_click=lambda: self.set_value(False)).props("dense")

    def on_pwd_entered(self, callback: Callable[[], None]):
        self._on_pwd_entereds.append(callback)
        return self

    def show(self):
        self.set_value(True)

    def check_password(self):
        try:
            enter_password(self._input_pwd.value)
        except ValueError:
            ui.notify("密码错误,请输入正确的文章密码")
            return

        self.set_value(False)
        for callback in self._on_pwd_entereds:
            callback()


class MyTabs(ui.column):
    def __init__(self) -> None:
        super().__init__()

        with self:
            self.build_tabs()

    @ui.refreshable_method
    def build_tabs(self):
        if need_show_pwd():
            return
        secret_codes = get_secret_codes()

        with ui.tabs() as tabs:
            for code in secret_codes:
                ui.tab(code.name)

        with ui.tab_panels(
            tabs, value=None if not secret_codes else secret_codes[0].name
        ):
            for code in secret_codes:
                with ui.tab_panel(code.name):
                    try:
                        load_ui(code)
                    except ValueError as e:
                        print(e)
                        ui.label("文章密码错误").classes("text-red-500")
                        ui.button("输入文章密码", on_click=pwd_dialog.show)


pwd_dialog = PwdDialog()


@pwd_dialog.on_pwd_entered
def on_pwd_entered():
    tabs.build_tabs.refresh()


if need_show_pwd():
    pwd_dialog.show()

tabs = MyTabs()

ui.run()
