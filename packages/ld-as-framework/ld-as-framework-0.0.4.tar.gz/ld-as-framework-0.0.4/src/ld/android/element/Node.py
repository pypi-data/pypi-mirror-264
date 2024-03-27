from ascript.android.node import Selector
from ..base.BaseProperties import AScriptQueryElement, Rect

class NodeQuery(AScriptQueryElement, Selector):
    """
    节点查询对象
    """
    pass

class Node:
    """
       控件返回的节点，其属性如下

          id            控件ID 部分APP中ID属性,随手机安装可能动态变化,谨慎使用

          text          控件的文本

          type          控件的类型

          desc          控件的描述

          hintText      控件的默认展示文本

          packageName   控件所属包名

          childCount    子控件数量

          inputType     输入类型

          maxTextLength 控件最大文本长度

          drawingOrder  是否可点击

          checkable     是否可选中

          checked       是否已选中

          editable      是否支持编辑

          enabled       是否可访问

          visible       是否针对用户展示

          dismissable   是否可取消

          focusable     是否可以获取焦点

          focused       是否已获取了焦点

          longClickable 是否可以长按
       """

    def __init__(self, node):
        self.id = node.id
        self.text = node.text
        self.type = node.type
        self.desc = node.desc
        self.hintText = node.hintText
        self.packageName = node.packageName
        self.childCount = node.childCount
        self.inputType = node.inputType
        self.maxTextLength = node.maxTextLength
        self.drawingOrder = node.drawingOrder
        self.checkable = node.checkable
        self.checked = node.checked
        self.editable = node.editable
        self.enabled = node.enabled
        self.visible = node.visible
        self.dismissable = node.dismissable
        self.focusable = node.focusable
        self.focused = node.focused
        self.longClickable = node.longClickable
        self.rect = Rect(node.rect)
        self.click = node.click
        self.long_click = node.long_click
        self.input = node.input

    def click(self):
        pass

    def long_click(self):
        pass

    def input(self):
        pass