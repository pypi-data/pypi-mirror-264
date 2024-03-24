import json

import allure


class ValidateObj(object):
    def __init__(self):
        self.validate_on_off = ""
        self.request = ""
        self.response = ""
        self.step_name = ""

    def validate_onoff(self, validate_on_off, step_name):
        self.validate_on_off = validate_on_off
        self.step_name = step_name

    def validate(self, request, response):
        self.request = request
        self.response = response
        if not self.validate_on_off:
            with allure.step(self.step_name):
                allure.attach(json.dumps(self.request, ensure_ascii=False, indent=4), "请求",
                              allure.attachment_type.JSON)
                allure.attach(json.dumps(self.response, ensure_ascii=False, indent=4), "响应",
                              allure.attachment_type.JSON)
                allure.attach("", "此步骤无断言",
                              allure.attachment_type.TEXT)

    def validate1(self, assert_data):
        with allure.step(self.step_name):
            allure.attach(json.dumps(self.request, ensure_ascii=False, indent=4), "请求", allure.attachment_type.JSON)
            allure.attach(json.dumps(self.response, ensure_ascii=False, indent=4), "响应", allure.attachment_type.JSON)
            allure.attach(str(assert_data), "断言", allure.attachment_type.TEXT)


obj = ValidateObj()

