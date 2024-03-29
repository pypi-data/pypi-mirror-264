from toolboxv2.utils.extras import Style

from .types import Result, ToolBoxInterfaces, ToolBoxError, ToolBoxInfo, ToolBoxResult
from .getting_and_closing_app import get_app
from .tb_logger import get_logger
from .all_functions_enums import CLOUDM_AUTHMANAGER


class MainTool:
    toolID: str = ""
    # app = None
    interface = None
    spec = ""

    def __init__(self, *args, **kwargs):
        self.version = kwargs["v"]
        self.tools = kwargs.get("tool", {})
        self.name = kwargs["name"]
        self.logger = kwargs.get("logs")
        if self.logger is None:
            self.logger = get_logger()
        self.color = kwargs.get("color", "WHITE")
        self.todo = kwargs.get("load", lambda: None)
        self._on_exit = kwargs.get("on_exit", lambda: None)
        self.stuf = False
        if not hasattr(self, 'config'):
            self.config = {}
        self.user = None
        self.description = "A toolbox mod" if kwargs.get("description") is None else kwargs.get("description")
        if MainTool.interface is None:
            MainTool.interface = self.app.interface_type
        # Result.default(self.app.interface)
        self.load()

    @property
    def app(self):
        return get_app(from_=f"{self.spec}.{self.name}|{self.toolID if self.toolID else '*'+MainTool.toolID} {self.interface if self.interface else MainTool.interface}")

    @app.setter
    def app(self, v):
        raise PermissionError(f"You cannot set the App Instance! {v=}")

    @staticmethod
    def return_result(error: ToolBoxError = ToolBoxError.none,
                      exec_code: int = 0,
                      help_text: str = "",
                      data_info=None,
                      data=None,
                      data_to=None):

        if data_to is None:
            data_to = MainTool.interface if MainTool.interface is not None else ToolBoxInterfaces.cli

        if data is None:
            data = {}

        if data_info is None:
            data_info = {}

        return Result(
            error,
            ToolBoxResult(data_info=data_info, data=data, data_to=data_to),
            ToolBoxInfo(exec_code=exec_code, help_text=help_text)
        )

    def load(self):
        if self.todo:
            try:
                self.todo()
            except Exception as e:
               get_logger().error(f" Error loading mod {self.name} {e}")
        else:
            get_logger().info(f"{self.name} no load require")

        self.app.print(f"TOOL : {self.spec}.{self.name} online")

    def print(self, message, end="\n", **kwargs):
        if self.stuf:
            return

        self.app.print(Style.style_dic[self.color] + self.name + Style.style_dic["END"] + ":", message, end=end,
                       **kwargs)

    def add_str_to_config(self, command):
        if len(command) != 2:
            self.logger.error('Invalid command must be key value')
            return False
        self.config[command[0]] = command[1]

    def webInstall(self, user_instance, construct_render) -> str:
        """"Returns a web installer for the given user instance and construct render template"""

    def get_user(self, username: str) -> Result:
        return self.app.run_any(CLOUDM_AUTHMANAGER.GET_USER_BY_NAME, username=username, get_results=True)

