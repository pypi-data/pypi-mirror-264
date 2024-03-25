from jinja2 import Template


def rend_template_str(t_str: str, *args, **kwargs):
    """
    渲染模板字符串

    参数:
    t_str (str): 模板字符串
    *args: 位置参数
    **kwargs: 关键字参数

    返回:
    str: 渲染后的字符串
    """

    # 创建模板对象
    t = Template(t_str, variable_start_string="${", variable_end_string="}")
    # 渲染模板
    res = t.render(*args, **kwargs)

    # 如果模板字符串以 '${' 开头，以 '}' 结尾
    if t_str.startswith("${") and t_str.endswith("}"):
        try:
            # 使用 eval 函数将渲染结果转换为表达式并计算
            return eval(res)
        except Exception:  # noqa
            # 如果计算出错，则返回渲染结果
            return res
    else:
        # 如果模板字符串不以 '${' 开头，以 '}' 结尾，则返回原值
        return res


def rend_template_obj(t_obj: dict, *args, **kwargs):
    """
    如果传dict对象，那么就通过模版字符串递归查找模版字符串，并转换成新的数据
    """
    if isinstance(t_obj, dict):
        for key, value in t_obj.items():
            if isinstance(value, str):
                t_obj[key] = rend_template_str(value, *args, **kwargs)
            elif isinstance(value, dict):
                t_obj[key] = rend_template_obj(value, *args, **kwargs)
            elif isinstance(value, list):
                t_obj[key] = rend_template_array(value, *args, **kwargs)
            else:
                pass
    return t_obj


def rend_template_array(t_array: list, *args, **kwargs):
    """
    如果传list对象，那么就通过模版字符串递归查找模版字符串，并转换成新的数据
    """
    if isinstance(t_array, list):
        new_array = []
        # 遍历t_array中的每个元素
        for item in t_array:
            # 如果元素是str类型
            if isinstance(item, str):
                # 调用rend_template_str函数，将item作为第一个参数，args作为其他参数，kwargs作为关键字参数，并将返回值添加到new_array中
                new_array.append(rend_template_str(item, *args, **kwargs))
            # 如果元素是dict类型
            elif isinstance(item, dict):
                # 调用rend_template_obj函数，将item作为第一个参数，args作为其他参数，kwargs作为关键字参数，并将返回值添加到new_array中
                new_array.append(rend_template_obj(item, *args, **kwargs))
            # 如果元素是list类型
            elif isinstance(item, list):
                # 调用rend_template_array函数，将item作为第一个参数，args作为其他参数，kwargs作为关键字参数，并将返回值添加到new_array中
                new_array.append(rend_template_array(item, *args, **kwargs))
            # 如果元素不是str、dict或list类型
            else:
                # 将元素添加到new_array中
                new_array.append(item)
        return new_array
    return t_array


def rend_template_any(t_any, *args, **kwargs):
    """
    如果传any对象，那么就通过模版字符串递归查找模版字符串，并转换成新的数据
    """
    if isinstance(t_any, str):
        return rend_template_str(t_any, *args, **kwargs)
    elif isinstance(t_any, dict):
        return rend_template_obj(t_any, *args, **kwargs)
    elif isinstance(t_any, list):
        return rend_template_array(t_any, *args, **kwargs)
    else:
        return t_any
