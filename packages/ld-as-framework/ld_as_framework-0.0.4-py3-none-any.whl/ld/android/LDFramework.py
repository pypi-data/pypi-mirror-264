from ..common import Logger

log = Logger.get_logger()


class LDFramework:
    """
    零动框架操作类
    """

    def __init__(self, elements: dict):
        self.elements = elements

    def _get_query_element(self, *args):
        """
        获取查询元素的对象
        :param args: 元素特征值
        :return: 元素查询对象
        """
        pass
        pass
        pass

    def element(self, *args: str):
        """
        获取元素的方法，可以利用获取的元素进行一系列操作
        :param args:元素特征信息
        :return:元素操作对象
        """
        pass
        pass
        pass

    def click_ele(self, element: list, r=5):
        """
        点击某个元素
        :param element: 需要点击的元素信息
        :param r: 随机范围
        :return:
        """
        pass

    def wait_element(self, element: list, timeout=3):
        """
        等待元素出现
        :param element:需要等待的元素特征信息
        :param timeout:等待的时间
        """
        pass

    def get_element(self, *args):
        """
        获取元素
        :param args:元素特征信息
        """
        pass

    @staticmethod
    def click(x, y, r=5):
        """
        点击坐标
        :param x: X轴
        :param y: Y轴
        :param r: 偏移像素
        """
        pass
        pass
        pass
        pass
        pass
        pass

    @staticmethod
    def swipe(from_point: [int, int], to_point: [int, int], timeout=1, will_continue=False, level=0.07):
        """
        滑动的方法，从一个点滑动到另外一个点
        :param level: 弯曲等级，数字越大就越弯曲，不要超过0.1
        :param from_point: 开始的点
        :param to_point: 结束的点
        :param timeout: 整个过程的时间，单位（秒）
        :param will_continue: 滑动完成后是否抬起手指
        :return:
        """
        pass
        pass
        pass
        pass
        pass
        pass
        pass
        pass
        pass

    @staticmethod
    def execute_with_timeout(timeout, func, *args, **kwargs):
        """
        执行指定函数,在给定的超时时间后结束执行

        :param timeout: 超时时间(秒)
        :param func: 要执行的函数
        :param args: 传递给函数的位置参数
        :param kwargs: 传递给函数的关键字参数
        """
        pass
        pass
        pass


class 零动框架:

    def __init__(self, 特征库: dict):
        self.framework = LDFramework(特征库)

    def 元素_操作(self, *args: str):
        """
        获取元素的方法，可以利用获取的元素进行一系列操作
        :param args:元素特征信息
        :return:元素操作对象
        """
        pass

    def 获取_元素(self, *args):
        """
        获取元素
        :param args:元素特征信息
        """
        pass

    @staticmethod
    def 点击_坐标(x, y, r=5):
        """
        点击坐标
        :param x: X轴
        :param y: Y轴
        :param r: 偏移像素
        """
        pass

    def 点击_元素(self, element: list, r=5):
        """
        点击某个元素
        :param element: 需要点击的元素信息
        :param r: 随机范围
        :return:
        """
        pass

    @staticmethod
    def 滑动(from_point: [int, int], to_point: [int, int], timeout=1, will_continue=False, level=0.07):
        """
        滑动的方法，从一个点滑动到另外一个点
        :param level: 弯曲等级，数字越大就越弯曲，不要超过0.1
        :param from_point: 开始的点
        :param to_point: 结束的点
        :param timeout: 整个过程的时间
        :param will_continue: 滑动完成后是否抬起手指
        :return:
        """
        pass

    def 等待_元素(self, element: list, timeout=3):
        """
        等待元素出现
        :param element:需要等待的元素特征信息
        :param timeout:等待的时间
        """
        pass
