from time import sleep
from ascript.android.node import Selector
from .CommonClass import CommonAction, Method
from ..element.Node import NodeQuery, Node
from ...common import Logger
log = Logger.get_framework_logger()

class NodeActionStrategy(CommonAction):
    """
    节点操作对象
    """

    def __init__(self, selector: NodeQuery, eleName, framework):
        super().__init__()
        self._selector = selector
        self._eleName = eleName
        self._framework = framework
        log.debug(f'实例化了NodeActionStrategy对象，元素名：{eleName}')

    def _find(self):
        pass
        pass
        pass
        pass
        pass

    def _node(self) -> Node:
        pass
        pass

    def click_node(self):
        """
        点击查询到的节点信息，如果没有查询到则不点击
        """
        pass
        pass

    def 点击_节点(self):
        """
        点击查询到的节点信息，如果没有查询到则不点击
        """
        pass

    def _click_node(self):
        pass
        pass
        pass

    def long_click(self):
        """
        长安查询到的节点信息，如果没有查询到则不执行
        """
        pass
        pass

    def 长按_节点(self):
        """
        长安查询到的节点信息，如果没有查询到则不执行
        """
        pass

    def _long_click(self):
        pass
        pass
        pass

    def input(self, msg: str):
        """
        长安查询到的节点信息，如果没有查询到则不执行
        """
        pass
        pass

    def 输入_文本(self, msg: str):
        """
        对查询到的节点信息输入文本
        """
        pass

    def _input(self, msg):
        pass
        pass
        pass