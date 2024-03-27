from ..base.BaseProperties import AScriptQueryElement, Rect

class ColorQuery(AScriptQueryElement):

    def __init__(self, colors: str):
        super().__init__()
        self.properties['colors']: str = colors
        self.properties['rect']: list | None = None
        self.properties['space']: int = 5
        self.properties['ori']: int = 2
        self.properties['diff']: float = 0.9

    def rect(self, x, y, x1, y1):
        """
        找色范围
        :param x: 左上角x
        :param y: 左上角y
        :param x1: 右下角x
        :param y1: 右下角y
        """
        pass
        pass

    def space(self, space: int=5):
        """
        找色结果间距,如果返回的结果,多个点位的像素值 在5像素内重合.则只保留一个
        :param space:找色结果间距 默认:5像素
        :return:
        """
        pass
        pass

    def ori(self, ori: int=2):
        """
        找色方向2(默认):左上角到右下角，横向开始找色
        :param ori: 找色方向 1-8 个方向
        """
        pass
        pass

    def diff(self, diff: float=0.9):
        """
        相似度, 取值范围0-1，1为100%匹配 默认:0.9
        :param diff: 相似度，取值范围0-1
        :return:
        """
        pass
        pass

class Color:

    def __init__(self, point, framework, find_range: [int, int, int, int]=None):
        self._framework = framework
        self.rect = Rect(centerX=point.x, centerY=point.y)
        if find_range is not None:
            x_mid = (find_range[0] + find_range[2]) / 2
            y_mid = (find_range[1] + find_range[3]) / 2
            self.rect = Rect(left=point.x, top=point.y, centerX=x_mid, centerY=y_mid)

    def click(self):
        pass