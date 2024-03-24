# 校验入口
from .log import log
from .extract import extract_by_object


def validate_response(response, validate_value):
    assert_result = []
    for check in validate_value:
        for check_type, check_value in check.items():
            expect_value = check_value[1]  # 获取期望值
            response_value = extract_by_object(
                response, check_value[0]
            )  # 获取相应字段响应结果
            log.info(f"断言公式：{check}")
            log.info(
                f"断言结果-> {check_type}: [预期结果：{expect_value},"
                f"实际结果：{response_value}]"
            )
            assert_result.append(f"断言结果-> {check_type}: [预期结果：{expect_value},"
                                 f"实际结果：{response_value}]")
            if check_type in ["eq", "="]:
                equals(response_value, expect_value)
            elif check_type in ["lt", "<"]:
                less_than(response_value, expect_value)
            elif check_type in ["lte", "<="]:
                less_than_or_equal(response_value, expect_value)
            elif check_type in ["gt", ">"]:
                greater_than(response_value, expect_value)
            elif check_type in ["gte", ">="]:
                greater_than_or_equal(response_value, expect_value)
            elif check_type in ["ne", "!="]:
                not_equal(response_value, expect_value)
            elif check_type in ["not_none", "notNone"]:
                not_none(response_value)
            elif check_type in ["startswith", "sw"]:
                starts_with(response_value, expect_value)
            elif check_type in ["endswith", "ew"]:
                ends_with(response_value, expect_value)
    return assert_result


def equals(response_value, expect_value):
    assert (
            response_value == expect_value
    ), f"(断言不通过：{response_value} == {expect_value})"


def less_than(response_value, expect_value):
    assert (
            response_value < expect_value
    ), f"(断言不通过：{response_value} < {expect_value})"


def less_than_or_equal(response_value, expect_value):
    assert (
            response_value <= expect_value
    ), f"(断言不通过：{response_value} <= {expect_value})"


def greater_than(response_value, expect_value):
    assert (
            response_value > expect_value
    ), f"(断言不通过：{response_value} > {expect_value})"


def greater_than_or_equal(response_value, expect_value):
    assert (
            response_value >= expect_value
    ), f"(断言不通过：{response_value} >= {expect_value})"


def not_equal(response_value, expect_value):
    assert (
            response_value != expect_value
    ), f"(断言不通过：{response_value} != {expect_value})"


def not_none(response_value):
    assert response_value is not None, f"(断言不通过：{response_value} is not None)"


# def contains(response_value, expect_value):
#     if isinstance(response_value, (list, tuple, dict, str)):
#         assert response_value in response_value, f'{response_value} in {response_value})'
#     else:
#         # 数字类型包含
#         assert str(response_value) in response_value, f'{response_value} in {response_value})'


def starts_with(response_value, expect_value):
    assert response_value.startswith(
        expect_value
    ), f"(断言不通过：{expect_value} starts with {response_value})"


def ends_with(response_value, expect_value):
    assert response_value.endswith(
        expect_value
    ), f"(断言不通过：{expect_value} ends with {response_value})"
