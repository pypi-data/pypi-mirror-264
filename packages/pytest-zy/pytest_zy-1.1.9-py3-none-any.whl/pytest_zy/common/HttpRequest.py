import json
import mimetypes
import re
from pathlib import Path

import requests
import urllib3
from requests import Response
from requests_toolbelt import MultipartEncoder

from . import render_template_obj
from .log import log


class HttpSession(requests.Session):
    def __init__(self, base_url: str = None, timeout=10):  # baseurl默认为None
        super().__init__()
        self.base_url = base_url
        self.timeout = timeout

    @staticmethod
    def check_url(base_url: str, url: str) -> str:
        """
        检查并拼接基础URL和目标URL

        :param base_url: 基础URL字符串，应包含http或https协议
        :param url: 目标URL字符串，可以是相对路径或带完整协议的URL
        :return: 拼接后的完整URL字符串，如果输入有效则返回URL，否则返回错误信息
        """
        # 检查url是否已经包含http或https协议
        if re.compile(r"(http)(s?)(://)").match(url):
            return url
        elif base_url:
            # 检查base_url是否包含http或https协议
            if re.compile(r"(http)(s?)(://)").match(base_url):
                # 如果base_url包含协议，则拼接base_url和url
                return f"{base_url.rstrip('/')}/{url.lstrip('/')}"
            else:
                # 记录base_url缺少协议的错误日志
                log.error(f"{base_url} -->  base url do yo mean http:// or https://!")

        else:
            # 记录url无效或缺少base_url的错误日志
            log.error(f"{url} --> url invalid or base url missed!")

    def run_request(self, args, copy_value, kwargs) -> Response:
        copy_value["url"] = self.check_url(self.base_url, copy_value["url"])
        kwargs.update(args)
        request_value = render_template_obj.rend_template_any(copy_value, **kwargs)
        if "headers" in request_value:
            if "application/json" in request_value["headers"]["Content-Type"].split(';'):
                request_value["data"] = json.dumps(request_value["data"])
            elif request_value["headers"]["Content-Type"] == "multipart/form-data":
                for key, value in request_value["data"].items():
                    value_dir = Path(value)
                    if value_dir.is_file():
                        m = MultipartEncoder(
                            fields={
                                key: (
                                    value_dir.name,
                                    value_dir.open("rb"),
                                    mimetypes.guess_type(value_dir)[0],
                                )
                            }
                        )  # 构造文件上传，便可以使用data传参
                        request_value["data"] = m
                        request_value["headers"]["Content-Type"] = m.content_type
                    else:
                        log.error("文件不存在，请检查")

        log.info(f"<<<请求内容>>>{request_value}", )
        try:
            response = self.request(timeout=self.timeout, **request_value)
            log.info(
                f'<<<响应内容>>>, {getattr(response, "status_code")} {getattr(response, "text", "")},{getattr(response, "reason", "")}')
            # response_value = getattr(response, "json", {})
            response_value = response.json()
            from .allure_step_validate import obj
            obj.validate(request_value, response_value)
            return response
        except requests.exceptions.ConnectTimeout as e:
            log.error(f"{copy_value['url']}请求超时-> {e}")
        except requests.exceptions.ConnectionError as e:
            log.error(f"{copy_value['url']}连接错误-> {e}")
        except urllib3.exceptions.MaxRetryError as e:
            log.error(f"{copy_value['url']}请求超出最大重试次数-> {e}")
