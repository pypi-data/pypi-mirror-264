from ..action.CommonClass import CommonAction
from ..element.Image import Image

class ImageActionStrategy(CommonAction):
    """
    图片操作对象
    """

    def __init__(self, selector: Image, eleName, framework):
        super().__init__()