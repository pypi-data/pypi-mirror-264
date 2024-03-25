import types
from inspect import Parameter
from . import create_function, my_builtins
from .log import log
from .db import execute_db
from .run_yaml import *
from .allure_step_validate import obj


class RunYaml(object):
    def __init__(self, raw, module: types.ModuleType, g: dict):
        self.raw = raw
        self.module = module
        self.g = g  # 加载全局配置
        self.global_variables = {}  # 全局变量
        self.module_variables = {}  # 模块变量

    def run(self):
        if not self.raw.get("config"):
            self.raw["config"] = {}
        case = {}  # 创建一个空字典 case
        config_variables = self.raw.get("config").get("variables", {})
        config_parameters = self.raw.get("config").get("parameters", {})
        config_fixtures = self.raw.get("config").get("fixtures", [])
        config_hooks = self.raw.get("config").get("hooks", {})
        config_marks_str = self.raw.get("config").get("marks", []) or []
        config_marks = (
            config_marks_str.rstrip(",").split(",") if isinstance(config_marks_str, str) else config_marks_str)
        self.global_variables.update(__builtins__)  # noqa 内置函数加载
        self.global_variables.update(my_builtins.__dict__)  # 自定义函数加载
        db_obj = execute_db(self.g)  # 数据库连接
        self.global_variables.update(**self.g)
        self.global_variables.update(**db_obj)
        # 模块变量渲染,可以将${}替换成原函数执行
        self.module_variables = render_template_obj.rend_template_any(
            config_variables, **self.global_variables
        )
        if isinstance(self.module_variables, dict):
            self.global_variables.update(self.module_variables)
        config_parameters = render_template_obj.rend_template_any(
            config_parameters, **self.global_variables
        )
        config_fixtures = render_template_obj.rend_template_any(config_fixtures, **self.global_variables)
        config_parameters, config_fixtures = self.parameters_date(
            config_parameters, config_fixtures
        )
        # 遍历 self.raw 中的每个键值对
        for case_name, case_value in self.raw.items():
            if case_name == "config":
                continue
            # 如果 case_name 不是以 "test" 开头，则在前面添加 "test_"
            if not str(case_name).startswith("test"):
                case_name = "test_" + str(case_name)
            # 如果 case_value 是一个列表，则直接将 case_name 和 case_value 添加到 case 中
            if isinstance(case_value, list):
                case[case_name] = case_value
            # 如果 case_value 不是列表，则将其转换为列表，并将 case_name 和 case_value 添加到 case 中
            else:
                case[case_name] = [case_value]

            def run_yaml_case(args):
                log.info(f"开始执行文件：{self.module.__name__}.yml")
                log.info(f"variables-> {self.module_variables}")
                call_function_name = inspect.getframeinfo(
                    inspect.currentframe().f_back
                )[2]
                log.info(f"运行用例-> {call_function_name}")
                request_session = args.get('requests_function') or args.get('requests_module') or args.get(
                    'requests_session')
                for step in case[call_function_name]:
                    title_name = step.get("name", "未命名用例步骤")
                    log.info(f"执行用例步骤-> {title_name}")  # 测试步骤名称
                    response = None
                    replace_data = step.get("replace", "")
                    if step.get("validate"):
                        validate_on_off = True
                        obj.validate_onoff(validate_on_off, title_name)
                    else:
                        validate_on_off = False
                        obj.validate_onoff(validate_on_off, title_name)
                    step_actions = {
                        "api": lambda values: process_api_request(values, args, request_session, replace_data,
                                                                  config_hooks, self.global_variables),
                        "request": lambda values: process_request(value, args, request_session, config_hooks,
                                                                  self.global_variables),
                        "extract": lambda values: process_extraction(value, response, self.global_variables,
                                                                     self.module_variables),
                        "validate": lambda values: process_validation(value, response,
                                                                      self.global_variables)
                    }
                    for item, value in step.items():
                        response = step_actions.get(item) and step_actions[item](value)

            f = create_function.create_function_from_parameters(
                func=run_yaml_case,
                parameters=self.function_parameters(
                    config_fixtures
                ),  # 向用例中加入fixture数据
                documentation=case_name,
                func_name=case_name,
                func_filename=f"{self.module.__name__}.py",
            )
            case_marks_str = case_value[0].get("marks", []) or []
            case_marks = (case_marks_str.rstrip(",").split(",") if isinstance(case_marks_str, str) else case_marks_str)
            marks = case_marks + config_marks
            if marks:
                # 依次添加标记到函数上
                for mark in marks:
                    import pytest
                    f = getattr(pytest.mark, mark)(f)
                # 将带有多个标记的函数添加到模块中
                setattr(self.module, str(case_name), f)
                # print(self.module.__dict__)  # 打印模块中的所有属性

            else:
                # 如果没有标记，直接添加原始函数
                setattr(self.module, str(case_name), f)
            if config_parameters:
                # 向 module 中加参数化数据的属性
                setattr(self.module, "params_data", config_parameters)

    @staticmethod
    def function_parameters(config_fixtures) -> list:
        function_parameters = [
            Parameter("request", Parameter.POSITIONAL_OR_KEYWORD),
        ]
        if not config_fixtures:
            function_parameters.append(Parameter("requests_session", Parameter.POSITIONAL_OR_KEYWORD))
        else:
            if "requests_function" in config_fixtures:
                function_parameters.append(Parameter("requests_function", Parameter.POSITIONAL_OR_KEYWORD))
            elif "requests_module" in config_fixtures:
                function_parameters.append(Parameter("requests_module", Parameter.POSITIONAL_OR_KEYWORD))
            else:
                function_parameters.append(Parameter("requests_session", Parameter.POSITIONAL_OR_KEYWORD))
            for key in config_fixtures:
                if key not in ["requests_function", "requests_module"]:
                    function_parameters.append(Parameter(key, Parameter.POSITIONAL_OR_KEYWORD))
        return function_parameters

    @staticmethod
    def parameters_date(parameters, config_fixtures) -> (list, list):
        parameters_values = []
        if isinstance(config_fixtures, str):
            # 字符串切成list
            config_fixtures = [item.strip(" ") for item in config_fixtures.split(',')]
        if isinstance(parameters, dict) and parameters.get("on_off", False):
            parameters.pop("on_off")
            parameters_values.extend(list(parameters.values()))
            config_fixtures.extend(list(parameters.keys()))
            return parameters_values, config_fixtures
        else:
            return [], config_fixtures
