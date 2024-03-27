class AScriptQueryElement:

    def __init__(self):
        self.properties = {}

    def get_param(self):
        pass

    def get_point(self):
        pass

class Rect:
    """
    获取控件在屏幕中的位置

    left x坐标

    top y坐标

    width 控件的宽度

    height 控件的高度

    centerX 控件的中心坐标X

    centerY 控件的中心坐标Y
    """

    def __init__(self, rect=None, left=None, top=None, width=None, height=None, centerX=None, centerY=None):
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.centerX = centerX
        self.centerY = centerY
        if rect is not None:
            self.left = rect.left
            self.top = rect.top
            self.width = rect.width()
            self.height = rect.height()
            self.centerX = rect.centerX()
            self.centerY = rect.centerY()