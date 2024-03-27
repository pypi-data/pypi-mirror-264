import time
from ..base.BaseProperties import Rect
from ..element.Image import Image
from ..element.Color import Color
from ..element.Node import Node
from ...common import Logger
log = Logger.get_framework_logger()

class Method:

    def __init__(self, target, *args, **kwargs):
        self.target = target
        self.args = args
        self.kwargs = kwargs

    def execute(self):
        pass

class CommonAction:

    def __init__(self):
        self._eleName = None
        self._chain: list[Method] = []
        self._status: bool = True
        self._framework = None
        self._rect: Rect | None = None
        self._ele_target: Image | Color | Node | None = None

    def find(self):
        pass
        pass

    def 查询(self):
        pass

    def _find(self):
        pass

    def get_element(self):
        """
        获取查询到的元素信息
        :return: 元素信息
        """
        pass
        pass
        pass
        pass

    def 获取_元素(self):
        """
        获取查询到的元素信息
        :return: 元素信息
        """
        pass

    def execute(self, sleep=0.5, loop=1):
        """
        执行动作链
        :param sleep: 执行一次延迟时间，单位（秒）
        :param loop:执行次数
        """
        pass
        pass
        pass

    def 执行(self, sleep=0.5, loop=1):
        pass

    def element(self, *args: str):
        """
        查找一个元素，并可以执行后面的操作
        :param args:元素特征信息
        :return: 元素操作对象
        """
        pass
        pass

    def 元素_操作(self, *args: str):
        """
        查找一个元素，并可以执行后面的操作
        :param args:元素特征信息
        :return: 元素操作对象
        """
        pass

    def sleep(self, second):
        """
        延迟
        :param second:延迟时间，单位秒
        """
        pass
        pass

    def 延迟(self, second):
        """
        延迟
        :param second:延迟时间，单位秒
        """
        pass

    def click(self, r=5):
        pass
        pass

    def 点击(self, r=5):
        pass

    def _click(self, r):
        pass
        pass

    def wait_element(self, element: list, timeout=3):
        """
        等待元素出现
        :param element:需要等待的元素特征信息
        :param timeout:等待的时间
        """
        pass
        pass
        pass
        pass
        pass
        pass

    def 元素_等待(self, element: list, timeout=3):
        """
        等待元素出现
        :param element:需要等待的元素特征信息
        :param timeout:等待的时间
        """
        pass

    def swipe(self, from_point: [int, int], to_point: [int, int], timeout=1, will_continue=False):
        """
        执行一个滑动的动作
        :param from_point: 滑动起点
        :param to_point: 滑动终点
        :param timeout: 过程执行时间，单位(秒)
        :param will_continue: 结束时候是否抬起手指
        """
        pass
        pass

    def 滑动(self, from_point: [int, int], to_point: [int, int], timeout=1, will_continue=False):
        """
        执行一个滑动的动作
        :param from_point: 滑动起点
        :param to_point: 滑动终点
        :param timeout: 过程执行时间
        :param will_continue: 结束时候是否抬起手指
        """
        pass

    def _swipe(self, from_point, to_point, timeout=1, will_continue=True):
        pass