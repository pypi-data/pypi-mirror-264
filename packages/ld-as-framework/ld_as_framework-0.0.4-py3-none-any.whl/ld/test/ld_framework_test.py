from time import sleep
from ..android.element.Color import ColorQuery
from ..android.LDFramework import LDFramework, 零动框架
from ascript.android.node import Selector
elements = {'任务1': {'系统应用': Selector().desc('文件夹：系统应用'), '系统应用2': Selector().desc('文件夹：系统应用2'), '设置': Selector().type('TextView').text('设置'), '输入框': Selector().text('三国云梦录').type('EditText'), '系统应用_颜色': ColorQuery('327,1046,#8275FF|370,1046,#359CFA|373,1001,#FDFDFD').rect(296, 969, 400, 1078)}, '系统菜单': {'系统应用': Selector().desc('文件夹：系统应用'), '设置': Selector().type('TextView').text('设置'), '系统': Selector().type('TextView').text('系统')}}
ld = LDFramework(elements)
ld2 = 零动框架(elements)
res = ld2.获取_元素('任务1', '系统应用_颜色')
print(res)