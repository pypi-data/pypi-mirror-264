from ascript.android.screen import FindColors
from .CommonClass import CommonAction
from ..element.Color import ColorQuery, Color
from ...common import Logger
log = Logger.get_logger()

class ColorActionStrategy(CommonAction):
    """
    颜色操作对象
    """

    def __init__(self, selector: ColorQuery, eleName, framework):
        super().__init__()
        self._selector = selector
        self._eleName = eleName
        self._framework = framework
        log.debug(f'实例化了ColorActionStrategy对象，元素名：{eleName}')

    def _find(self):
        pass
        pass
        pass
        pass
        pass
        pass
        pass