from .log import log
import pymysql


class ConnectMysql(object):
    """
    连接MySQL数据库的类，使用单例模式确保全局仅有一个数据库连接实例。

    Attributes:
        instance (ConnectMysql): 单例实例，确保全局唯一。
        init_flag (bool): 标记是否已经初始化连接。
    """

    instance = None
    init_flag = False

    def __new__(cls, *args, **kwargs):
        """
        创建或返回ConnectMysql类的单例实例。

        Args:
            *args: 传递给类构造器的位置参数。
            **kwargs: 传递给类构造器的关键字参数。

        Returns:
            ConnectMysql的单例实例。
        """
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self, host, user, password, port, database):
        """
        初始化MySQL数据库连接。

        Args:
            host (str): 数据库主机地址。
            user (str): 连接数据库的用户名。
            password (str): 连接数据库的密码。
            port (int): 数据库服务的端口号。
            database (str): 要连接的数据库名。
        """
        if self.init_flag:
            return
        try:
            self.db = pymysql.connect(
                host=host,
                user=user,
                password=password,
                port=port,
                database=database,
                cursorclass=pymysql.cursors.DictCursor,  # 使用字典式游标，方便获取数据
            )
            self.cursor = self.db.cursor()  # 创建游标
            log.info(f"mysql connect success")  # 记录连接成功日志
        except Exception as e:
            self.cursor = None
            log.error(f"mysql connect error: {e}")  # 记录连接失败日志
        self.init_flag = True  # 标记连接初始化完成

    def query_sql(self, sql):
        if self.cursor:
            log.debug(f"mysql query sql: {sql}")
            try:
                self.cursor.execute(sql)  # 执行SQL语句
                result = self.cursor.fetchall()  # 返回查询结果
                if len(result) == 1:
                    result = result[0]
                elif len(result) == 0:
                    result = None
                log.info(f"mysql query result: {result}")
                return result
            except Exception as e:
                log.error(f"mysql query error: {e}")

    def execute_sql(self, sql):
        if self.cursor:
            log.info(f"mysql execute sql: {sql}")
            try:
                result = self.cursor.execute(sql)  # 执行SQL语句
                log.info(f"mysql result: {result} ")
            except Exception as e:
                log.error(f"mysql execute error: {e}")

    def close(self):
        """
        关闭数据库连接。
        """
        if self.cursor:
            self.cursor.close()
            self.db.close()
            log.info(f"mysql close success")


def execute_db(g):
    env_obj = g.get("env")
    if not hasattr(env_obj, "MYSQL_HOST"):
        return {
            "query_sql": lambda x: log.error("MYSQL_HOST not found in config.py"),
            "execute": lambda x: log.error("MYSQL_HOST not found in config.py"),
        }
    try:
        db = ConnectMysql(
            env_obj.MYSQL_HOST,
            env_obj.MYSQL_USER,
            env_obj.MYSQL_PASSWORD,
            env_obj.MYSQL_PORT,
            env_obj.MYSQL_DATABASE,
        )
        return {"query_sql": db.query_sql, "execute_sql": db.execute_sql}
    except Exception as e:
        log.error(f"mysql init error: {e}")
        return {
            "query_sql": lambda x: log.error("MYSQL connect error in config.py"),
            "execute_sql": lambda x: log.error("MYSQL connect error in config.py"),
        }
