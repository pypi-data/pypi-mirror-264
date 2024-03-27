import setuptools

import os
import ast
import shutil


class ReplaceMethodBodies(ast.NodeTransformer):
    def visit_FunctionDef(self, node):
        # 仅处理普通方法定义节点，排除构造函数等特殊方法
        if not node.name.startswith("__") or not node.name.endswith("__"):
            new_body = []
            # 记录方法注释
            method_comment = None
            for stmt in node.body:
                # 如果是注释节点，则记录方法注释
                if isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Str):
                    method_comment = stmt
                else:
                    if method_comment:
                        new_body.append(method_comment)
                        method_comment = None
                    # 将原始代码替换为pass
                    stmt = ast.Pass()
                    new_body.append(stmt)
            # 如果方法体以注释结尾，确保添加上该注释
            if method_comment:
                new_body.append(method_comment)
            node.body = new_body
        return node


def del_all_files(directory):
    if os.path.exists(directory) is False:
        return
    # 遍历目录中的所有文件和子目录
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            # 如果是文件，则删除
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            # 如果是目录，则递归删除
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'无法删除 {file_path}。原因: {e}')
    # 最后删除目录本身
    os.rmdir(directory)


def copy_pypirc():
    current_directory = os.getcwd()

    # 构建源文件的完整路径
    source_file = os.path.join(current_directory, '.pypirc')

    # 获取home目录的路径，这取决于操作系统
    # 在Unix/Linux/macOS上，通常是'/home/username'
    # 在Windows上，通常是'C:\\Users\\username'
    home_directory = os.path.expanduser('~')

    # 构建目标文件的完整路径
    destination_file = os.path.join(home_directory, '.pypirc')

    # 复制文件
    try:
        shutil.copy(source_file, destination_file)
        print(f"成功复制鉴权文件到：{destination_file}")
    except PermissionError:
        print(f"没有权限写入目标位置 {destination_file}")
    except Exception as e:
        print(f"复制文件时发生错误: {e}")


def deal_project(source_dir, destination_dir):
    # 复制鉴权文件
    copy_pypirc()
    # 先删除之前的所有文件打包好的
    del_all_files(destination_dir)

    # 创建目标目录
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    # 遍历源目录中的所有文件和子目录
    for root, dirs, files in os.walk(source_dir):
        # 构建目标子目录路径
        relative_path = os.path.relpath(root, source_dir)
        target_dir = os.path.join(destination_dir, relative_path)

        # 创建目标子目录
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        # 遍历每个文件
        for file in files:
            # 检查文件扩展名是否为.py
            if file.endswith('.py'):
                # 构建源文件和目标文件路径
                source_file_path = os.path.join(root, file)
                target_file_path = os.path.join(target_dir, file)
                with open(source_file_path, 'r', encoding='utf-8') as f:
                    code = f.read()
                tree = ast.parse(code)
                transformer = ReplaceMethodBodies()
                new_tree = transformer.visit(tree)
                new_code = ast.unparse(new_tree)
                with open(target_file_path, 'w', encoding='utf-8') as f:
                    f.write(new_code)


source_directory = r"../ld"
destination_directory = r"ld-as-framework-framework"
# copy_pypirc()

deal_project(source_directory, destination_directory)
