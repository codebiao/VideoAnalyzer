import requests
import json
import time

class Analyzer():

    def __init__(self, analyzerHost):
        self.analyzerHost = analyzerHost
        self.timeout = 3

    def controls(self):
        """
        """
        __state = False
        __msg = "error"
        __data = []

        try:
            headers = {
                "Content-Type": "application/json;"
            }

            data = {
            }

            data_json = json.dumps(data)

            res = requests.post(url='%s/api/controls' % self.analyzerHost, headers=headers,
                                data=data_json, timeout=self.timeout)
            if res.status_code:
                res_result = res.json()
                __msg = res_result["msg"]
                if res_result["code"] == 1000:

                    res_result_data = res_result.get("data")
                    if res_result_data:
                        __data = res_result_data
                    __state = True

            else:
                __msg = "status_code=%d " % (res.status_code)

        except Exception as e:
            __msg = str(e)

        return __state, __msg, __data

    def control(self, code):
        """
        @code   布控编号    [str]  xxxxxxxxx
        """
        __state = False
        __msg = "error"
        __control = {}
        try:
            headers = {
                "Content-Type": "application/json;"
            }
            data = {
                "code": code,
            }

            data_json = json.dumps(data)
            res = requests.post(url='%s/api/control' % self.analyzerHost, headers=headers,
                                data=data_json, timeout=self.timeout)
            if res.status_code:
                res_result = res.json()
                __msg = res_result["msg"]
                if res_result["code"] == 1000:
                    __control = res_result.get("control")
                    __state = True

            else:
                __msg = "status_code=%d " % (res.status_code)

        except Exception as e:
            __msg = str(e)

        return __state, __msg, __control

    def control_add(self, code, behaviorCode, streamUrl, pushStream, pushStreamUrl):
        """
        @code          布控编号                    [str]  xxxxxxxxx
        @behaviorCode  布控的视频流处理算法          [str]ZHOUJIERUQIN
        @streamUrl     布控视频流的拉流地址          [str]rtmp://192.168.1.3:1935/live/m2
        @pushStream  布控的视频流经处理后是否推流      [bool] True
        @pushStreamUrl 布控的视频流经过处理的推流地址  [str]rtmp://192.168.1.3:1935/live/m2-behavior
        """
        __state = False
        __msg = "error"

        try:
            headers = {
                "Content-Type": "application/json;"
            }

            print("pushStream",type(pushStream),pushStream)


            data = {
                "code": code,
                "streamUrl": streamUrl,
                "pushStream": pushStream,
                "pushStreamUrl": pushStreamUrl,
                "behaviorCode": behaviorCode,
            }

            data_json = json.dumps(data)

            print(data_json)

            res = requests.post(url='%s/api/control/add' % self.analyzerHost, headers=headers,
                                data=data_json, timeout=self.timeout)
            if res.status_code:
                res_result = res.json()
                __msg = res_result["msg"]
                if res_result["code"] == 1000:
                    __state = True

            else:
                __msg = "status_code=%d " % (res.status_code)

        except Exception as e:
            __msg = str(e)

        return __state, __msg

    def control_cancel(self, code):
        """
        @code   布控编号    [str]  xxxxxxxxx
        """
        __state = False
        __msg = "error"

        try:
            headers = {
                "Content-Type": "application/json;"
            }
            data = {
                "code": code,
            }

            data_json = json.dumps(data)
            res = requests.post(url='%s/api/control/cancel' % self.analyzerHost, headers=headers,
                                data=data_json, timeout=self.timeout)
            if res.status_code:
                res_result = res.json()
                __msg = res_result["msg"]
                if res_result["code"] == 1000:
                    __state = True

            else:
                __msg = "status_code=%d " % (res.status_code)

        except Exception as e:
            __msg = str(e)

        return __state, __msg