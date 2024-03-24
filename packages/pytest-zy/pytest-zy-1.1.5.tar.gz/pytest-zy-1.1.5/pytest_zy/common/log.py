import logging
from datetime import datetime
from pathlib import Path

# 初始化日志记录器
# 参数：
#   __name__: 当前模块的名称，用于标识日志记录器来源
# 返回值：
#   log: 配置好的日志记录器实例
log = logging.getLogger(__name__)


def remove_log(log_dir: Path, count=4, suffix=".log"):
    """
    清楚多余的日志，只保留最近的4个日志
    """
    if isinstance(log_dir, Path):
        p = log_dir
    elif isinstance(log_dir, str):
        p = Path(log_dir)
    else:
        log.error(f"文件路径不合法：{log_dir}")
        return
    if not p.exists():
        log.error(f"文件路径不存在：{log_dir}")
        return

    # 步骤1：收集目录p中所有指定后缀的文件
    all_logs = [
        item for item in p.iterdir() if item.is_file() and item.suffix == suffix
    ]

    # 步骤2：按文件的创建时间倒序排序
    all_logs.sort(key=lambda x: x.stat().st_mtime, reverse=True)

    # 步骤3：从第count个文件开始，删除所有文件
    for item in all_logs[count:]:
        item.unlink()


def set_log_format(config):
    """
    设置日志格式。

    参数:
    - config: 配置对象，用于获取和设置配置信息。

    该函数根据配置情况，自动设定日志文件的路径、级别和格式，
    如果没有在配置中指定，则使用默认值。
    """
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    remove_log(log_dir=Path(config.rootdir).joinpath("logs"))
    # 设置日志文件路径，默认为logs目录下当前时间戳的log文件
    if not config.getini("log_file") and not config.getoption("log_file"):
        config.option.log_file = Path(config.rootdir).joinpath(
            "logs", f"{current_time}.log"
        )
    # 设置日志文件记录级别，默认为info
    if not config.getini("log_file_level") and not config.getoption("log_file_level"):
        config.option.log_file_level = "info"
    # 设置日志文件的格式，默认为包含时间、级别和消息的格式
    if config.getini(
        "log_file_format"
    ) == "%(levelname) - 8s %(name)s: %(filename)s:%(lineno)d %(message)s" and not config.getoptipn(
        "log_file_format"
    ):
        config.option.log_file_format = "%(asctime)s [%(levelname)s]: %(message)s"
    if not config.getini("log_file_format") and not config.getoption("log_file_format"):
        config.option.log_file_format = "%(asctime)s [%(levelname)s]: %(message)s"
    if config.getini("log_file_date_format") == "%H:%M:%S" and not config.getoption(
        "log_file_date_format"
    ):
        config.option.log_file_date_format = "%Y-%m-%d %H:%M:%S"
    if not config.getini("log_file_date_format") and not config.getoption(
        "log_file_date_format"
    ):
        config.option.log_file_date_format = "%Y-%m-%d %H:%M:%S"
