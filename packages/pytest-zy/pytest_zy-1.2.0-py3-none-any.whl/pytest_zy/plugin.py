import importlib
import time
import types
from pathlib import Path
from .common.ReportNotify import dingding_notify
from .common.log import set_log_format, log
import pytest
import yaml
from _pytest.python import Module
from .common import Runner, HttpRequest
from .common.create_function import import_from_file

g = {}  # 全局变量 从config.py中读取配置


@pytest.fixture(scope="session")
def requests_session(request):  # 调用内置fixture
    """
    获取当前测试用例的 session 属性。
    """
    s = HttpRequest.HttpSession()
    print("请求信息", request.config.option)
    s.base_url = request.config.option.base_url

    yield s

    s.close()


# @pytest.fixture(scope="module")
# def requests_session(request):  # 调用内置fixture
#     """
#     获取当前测试用例的 session 属性。
#     """
#     s = HttpRequest.HttpSession()
#     s.base_url = request.config.option.base_url
#
#     print("前置")
#     yield s
#     print("后置")
#     s.close()
# @pytest.fixture()
# def requests_function(request):  # 调用内置fixture
#     """
#     获取当前测试用例的 session 属性。
#     """
#     s = HttpRequest.HttpSession()
#     s.base_url = request.config.option.base_url
#
#     print("前置")
#     yield s
#     print("后置")
#     s.close()


def pytest_collect_file(file_path: Path, parent):
    # 获取文件.yml 文件,匹配规则
    if file_path.suffix == ".yml" and file_path.name.startswith("test"):
        pytest_module = Module.from_parent(parent, path=file_path)
        module = types.ModuleType(file_path.stem)  # 动态创建module
        with file_path.open(encoding="utf-8") as f:
            raw_dict = yaml.safe_load(f)
        if not raw_dict:
            return
        run = Runner.RunYaml(raw_dict, module, g)
        run.run()
        pytest_module._getobj = lambda: module  # noqa
        # items = pytest_module.collect()  # 收集所有测试项
        # for item in items:
        #     # 获取测试项的标记
        #     marks = [m.name for m in item.iter_markers()]
        #     item.add_marker(pytest.mark.smoke)
        #     print(f"测试用例: {item.name}")
        #     print(f"路径: {item.path}")
        #     print(f"类型: {type(item)}")
        #
        #     # 打印测试类和测试函数的元数据
        #     if isinstance(item, pytest.Class):
        #         print(f"测试类: {item.name}")
        #         print(f"文件路径: {item.fspath}")
        #         for method in item.collect():
        #             if method.name.startswith("test_"):
        #                 print(f"    测试函数: {method.name}")
        #                 print(f"    函数对象: {method.obj}")
        #     elif isinstance(item, pytest.Function):
        #         print(f"测试函数: {item.name}")
        #         print(f"函数标记: {item.obj }")
        return pytest_module


@pytest.fixture()
def clea():
    print("前置")
    yield
    print("后置")


@pytest.fixture()
def cle():
    print("前置1")
    yield
    print("后置1")


def pytest_generate_tests(metafunc):  # noqa
    """
    动态生成测试用例参数。

    此函数为 pytest 的钩子函数，用于根据模块级别的 `params_data` 属性动态生成测试参数。
    `params_data` 可以是一个列表或字典，其具体结构会影响生成的测试参数。

    :param metafunc: pytest 的 Metafunc 对象，包含了当前测试函数的元数据。
    """
    if hasattr(metafunc.module, "params_data"):
        # 获取 params_data 属性，它定义了测试参数信息
        params_data = getattr(metafunc.module, "params_data")
        params_len = 0  # 初始化参数化参数的个数

        # 根据 params_data 的类型和结构，计算参数化参数的个数
        if isinstance(params_data, list):
            if isinstance(params_data, list):
                params_len = len(params_data)
            elif isinstance(params_data, dict):
                params_len = len(params_data.keys())
            else:
                params_len = 1

        # 从 fixturenames 中获取与 params_data 对应的参数名
        params_args = metafunc.fixturenames[-params_len:]
        params_data = list(zip(*params_data))
        new_params = [list(i) for i in params_data]
        metafunc.parametrize(params_args, new_params, scope="function")


def pytest_addoption(parser):  # noqa
    # run env
    parser.addini(
        "env", default=None, help="run environment by test or uat ..."
    )  # 添加pytest.ini中的一个配置项
    parser.addoption(
        "--env", action="store", default=None, help="run environment by test or uat ..."
    )  # 添加命令行选项


def pytest_configure(config):
    """
    pytest 配置函数，在 pytest 初始化时被调用，用于配置测试运行环境。

    参数:
    - config: pytest 的配置对象，可以用来设置和获取各种配置信息。

    返回值:
    无
    """
    set_log_format(config)  # 设置日志格式
    g['root_path'] = config.rootpath
    config_path = Path(config.rootdir).joinpath("config.py")  # 获取配置文件路径
    if config_path.exists():
        # 如果配置文件存在，则读取环境配置
        run_env = config.getoption("--env") or config.getini(
            "env"
        )  # 从命令行参数或配置文件中获取运行环境
        config_module = import_from_file(config_path)  # 动态导入 config 模块
        if hasattr(config_module, "env"):  # 检查 config 模块是否定义了环境配置
            g["env"] = config_module.env[run_env]  # 将指定环境的配置保存到全局变量
            g["env_name"] = run_env  # 保存环境名称到全局变量

        if g.get("env"):
            g["base_url"] = g["env"].BASE_URL if g["env"].BASE_URL else None
        else:
            g["base_url"] = None
        if g["base_url"] is not None:
            config.option.base_url = g["base_url"]
            if hasattr(config, "_metadata"):
                config._metadata["base_url"] = g["base_url"]  # noqa


def pytest_terminal_summary(terminalreporter, exitstatus, config):  # noqa
    """
    在pytest测试终止时生成测试总结信息。

    参数:
    - terminalreporter: 一个终端报告器对象，用于获取测试统计信息。
    - exitstatus: 测试退出状态，表示测试运行的最终结果。
    - config: pytest的配置对象，可以用于获取配置信息。

    说明:
    该函数不返回任何内容，但会通过终端报告器打印测试的总结信息。
    """

    total = terminalreporter._numcollected  # noqa 获取收集到的测试总数
    if total > 0:
        # 计算通过、失败和错误的测试数量，排除在清理阶段发生的状况
        passed = len(
            [
                i
                for i in terminalreporter.stats.get("passed", [])
                if i.when != "teardown"
            ]
        )
        failed = len(
            [
                i
                for i in terminalreporter.stats.get("failed", [])
                if i.when != "teardown"
            ]
        )
        errors = len(
            [i for i in terminalreporter.stats.get("error", []) if i.when != "teardown"]
        )
        # 计算测试成功的百分比
        successful = (
                len(terminalreporter.stats.get("passed", []))
                / terminalreporter._numcollected
                * 100
        )  # noqa

        # 计算测试的总时长
        duration = time.time() - terminalreporter._sessionstarttime  # noqa
        message = f"""
本次测试执行结果:
- 总用例数量: {total}
- 通过: {passed}
- 失败: {failed}
- 错误: {errors}
- 总耗时: {duration: .2f}秒
- 总通过率: {successful:.2f}%
        """
        if g["env"].DINGDING_ON_OFF:
            dingding_notify(
                message,
                g["env"].DINGDING_WEBHOOK,
                g["env"].DINGDING_SECRET,
            )


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == 'call' and rep.failed:
        failure_info = rep.longrepr
        if hasattr(failure_info, 'reprcrash'):
            error_message = failure_info.reprcrash.message
        else:
            error_message = failure_info
        log.error(f"Test '{item.nodeid}' failed: {error_message}")
