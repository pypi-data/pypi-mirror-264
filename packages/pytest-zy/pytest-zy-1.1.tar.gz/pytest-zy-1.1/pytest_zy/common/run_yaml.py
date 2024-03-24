import copy
import inspect

import yaml
from jsonpath_ng import parse
from . import render_template_obj, exceptions
from .allure_step_validate import obj
from .extract import extract_by_object
from .log import log
from .validate import validate_response
from pathlib import Path


def replace_parameters(data, rpl):
    for replace_key, replace_value in rpl.items():
        jsonpath_expression = parse(f"$..{replace_key}")
        matches = [match for match in jsonpath_expression.find(data)]
        if matches:
            # 找到目标键后，替换对应的值
            for match in matches:
                match.full_path.update(data, replace_value)
            log.info(f"字段: '{replace_key}'的值->已被替换为:新值'{replace_value}'!")
        else:
            log.error(f"要替换的字段'{replace_key}' 不存在!")
    return data


def request_hooks(request_value, config_hooks, global_variables):
    funcs = []
    request_value_hooks = []  # 请求体中的hooks
    # 获取config中的request钩子
    if "request" in config_hooks and isinstance(config_hooks["request"], str):
        config_hooks["request"] = config_hooks.get("request").split(",")

    # 获取请求体中的request钩子
    if request_value.get("hooks", {}).get("request") and isinstance(request_value["hooks"]["request"], str):
        request_value_hooks = request_value["hooks"]["request"].split(",")
        request_value.pop("hooks", None)

    # 合并钩子
    funcs_name = config_hooks.get("request", []) + request_value_hooks

    for func_name in funcs_name:
        if global_variables.get(func_name):
            funcs.append(global_variables.get(func_name))
        else:
            log.error(f"函数{func_name}不存在")

    for func in funcs:
        ars = [arg_name for arg_name, v in inspect.signature(func).parameters.items()]  # 获取函数对象的入参
        if "request_value" in ars:
            func(request_value)
        else:
            func()


def process_api_request(value, args, request_session, replace_data, config_hooks, global_variables):
    root_dir = args.get("request").config.rootdir

    api_path = Path(root_dir).joinpath(value)

    replace_data = render_template_obj.rend_template_any(replace_data, **global_variables)
    try:
        with api_path.open(encoding="utf-8") as f:
            raw_api = yaml.safe_load(f)  # yaml接口文件中的原数据
    except FileNotFoundError as e:
        raise exceptions.RawValueError(f"接口文件'{api_path}'不存在，请检查")

    try:
        request_value = copy.deepcopy(raw_api["request"])
    except Exception:
        raise exceptions.RawValueError(f"接口文件'{api_path}'中request字段不存在，请检查")
    if replace_data:
        request_value = replace_parameters(request_value, replace_data)
    if config_hooks or "hooks" in request_value:
        request_hooks(request_value, config_hooks, global_variables)
    response = request_session.run_request(args, request_value, global_variables)
    return response


def process_request(request_value, args, request_session, config_hooks, global_variables):
    request_value = copy.deepcopy(request_value)
    if config_hooks or "hooks" in request_value:
        request_hooks(request_value, config_hooks, global_variables)
    response = request_session.run_request(args, request_value, global_variables)
    return response


def process_extraction(value, response, global_variables, module_variables):
    copy_value = copy.deepcopy(value)
    extract_render_value = render_template_obj.rend_template_any(copy_value, **global_variables)
    extract_result = {}
    for key, expression in extract_render_value.items():
        extract_value = extract_by_object(response, expression)
        extract_result[key] = extract_value
    module_variables.update(extract_result)
    global_variables.update(module_variables)
    return response


def process_validation(value, response, global_variables):
    validate_value = render_template_obj.rend_template_any(value, **global_variables)
    assert_result = validate_response(response, validate_value)
    obj.validate1(assert_result)
    return response
