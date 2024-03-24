import jsonpath

from .log import log


def extract_by_object(response, extract_expression: str):
    if not isinstance(extract_expression, str):
        return extract_expression
    res = {
        "headers": dict(response.headers),
        "cookies": dict(response.cookies),
    }
    if extract_expression in ["status_code", "url", "encoding", "ok"]:
        return getattr(response, extract_expression)
    elif extract_expression.startswith("headers") or extract_expression.startswith(
        "cookies"
    ):
        try:
            return extract_by_jsonpath(res, extract_expression)
        except Exception as e:
            raise Exception(f"expression: {extract_expression}, error: {e}")
    elif extract_expression.startswith("$."):
        try:
            return extract_by_jsonpath(response.json(), extract_expression)
        except Exception as e:
            raise Exception(f"expression: {extract_expression}, error: {e}")
    else:
        # 其它非取值表达式，直接返回
        return extract_expression


def extract_by_jsonpath(json_value: dict, extract_expression: str):
    """
    使用JsonPath表达式从JSON对象中提取值。

    参数:
    json_value: dict - 待提取值的JSON对象。
    extract_expression: str - JsonPath表达式，用于指定要提取的值。
    返回值:
    如果找到匹配的值，返回该值；如果找到多个值，返回第一个值；如果没有找到值，返回None。
    """
    # 检查提取表达式是否为字符串
    if not isinstance(extract_expression, str):
        return extract_expression

    # 使用JsonPath表达式提取值
    extract_value = jsonpath.jsonpath(json_value, extract_expression)

    # 如果没有提取到值，返回None
    if not extract_value:
        log.error(f"JsonPath提取表达式[{extract_expression}]，没有找到匹配的字段。")
        return
    # 如果提取到一个值，返回该值
    elif len(extract_value) == 1:
        log.info(f"表达式[{extract_expression}]提取的变量为: {extract_value}")
        return extract_value[0]
    else:
        return extract_value
