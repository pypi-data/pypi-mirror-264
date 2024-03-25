import sys
import types
from typing import Any, Callable, Mapping, Sequence
from inspect import Parameter, Signature


def create_function_from_parameters(
    func: Callable[[Mapping[str, Any]], Any],
    parameters: Sequence[Parameter] = None,
    documentation=None,
    func_name=None,
    func_filename=None,
):
    """
    动态创建函数
    :param func: callback 回调函数
    :param parameters: 调用函数的参数
    :param documentation: 函数描述文档
    :param func_name: 函数名称
    :param func_filename: 函数文件名称
    :return: 返回函数对象function obj
    """
    new_signature = Signature(parameters)  # 根据参数生成新的签名

    # 定义一个内部函数，用于返回局部变量的字典
    def pass_locals():
        return dict_func(locals())  # noqa: F821

    # 获取内部函数的字节码对象
    code = pass_locals.__code__

    # 计算模块字节码的参数数量、局部变量数量、局部变量名称列表
    mod_co_arg_count = len(parameters)
    mod_co_n_locals = len(parameters)
    mod_co_var_names = tuple(param.name for param in parameters)

    # 设置模块字节码的名称和文件名
    mod_co_name = func_name or code.co_name

    # 如果函数名存在，则使用函数名作为模块的名称
    if func_filename:
        # 使用函数所在的文件名作为模块的文件名
        mod_co_filename = func_filename
        # 将模块的第一行代码的行号设置为1
        mod_co_first_lineno = 1
    else:
        # 使用代码对象的文件名作为模块的文件名
        mod_co_filename = code.co_filename
        # 使用代码对象的第一行代码的行号作为模块的第一行代码的行号
        mod_co_first_lineno = code.co_firstlineno

    # 根据Python版本生成修改后的字节码对象
    # 如果当前Python版本大于等于3.8
    if sys.version_info >= (3, 8):
        # 修改后的代码
        modified_code = code.replace(
            co_argcount=mod_co_arg_count,  # 函数参数数量
            co_nlocals=mod_co_n_locals,  # 函数局部变量数量
            co_varnames=mod_co_var_names,  # 函数变量名称列表
            co_name=mod_co_name,  # 函数名称
            co_filename=mod_co_filename,  # 函数文件名
            co_firstlineno=mod_co_first_lineno,  # 函数第一行的行号
        )
    else:
        # 修改后的代码
        modified_code = types.CodeType(
            mod_co_arg_count,  # 函数参数数量
            code.co_kwonlyargcount,  # 函数关键字参数数量
            mod_co_n_locals,  # 函数局部变量数量
            code.co_stacksize,  # 函数栈大小
            code.co_flags,  # 函数标志
            code.co_code,  # 函数字节码
            code.co_consts,  # 函数常量列表
            code.co_names,  # 函数名称列表
            mod_co_var_names,  # 函数变量名称列表
            mod_co_filename,  # 函数文件名
            mod_co_name,  # 函数名称
            mod_co_first_lineno,  # 函数第一行的行号
            code.co_lnotab,  # 函数行号和字节码的映射表
        )

    # 获取所有参数的默认值，并将非空默认值组成的元组赋值给defaults变量
    default_arg_values = tuple(
        p.default for p in parameters if p.default != Parameter.empty
    )

    """
    创建一个新的函数对象
    使用types.FunctionType创建一个函数对象
    modified_code是函数的代码
    'dict_func'是函数的参数名，func是函数的值
    'locals'是函数的局部变量
    name是函数的名称
    argdefs是函数的默认参数值
    """
    modified_func = types.FunctionType(
        modified_code,
        {"dict_func": func, "locals": locals},
        name=func_name,
        argdefs=default_arg_values,
    )

    # 设置函数的文档字符和签名
    modified_func.__doc__ = documentation
    modified_func.__signature__ = new_signature
    return modified_func


def import_from_file(filename):
    """载入 config 文件"""
    d = types.ModuleType("config")  # 创建一个模块对象
    d.__file__ = filename
    try:
        with open(filename, "r", encoding="utf-8") as config_file:
            exec(compile(config_file.read(), filename, "exec"), d.__dict__)
    except ImportError as e:
        print("fail to read config file: {}".format(filename))
        raise e
    return d
