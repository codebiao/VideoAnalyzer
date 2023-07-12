print("Algorithm.py")
import sys
import os

root_path = os.path.dirname(__file__)

sys.path.append(root_path+"/venv/Lib/site-packages")
sys.path.append(root_path+"/venv/Scripts")

# root_path = os.path.dirname(__file__)
# sys.path.append(root_path+"/Python/Lib/site-packages")
# sys.path.append(root_path+"/Python/DLLs")
# sys.path.append(root_path+"/Python/Scripts")

paths = sys.path
print("sys.paths , 共计%d条路径"%(len(paths)))
for p in paths:
    print("\t", p)

import json
import cv2
import numpy as np
import base64
from lib.OpenVinoYoloV5Detector import OpenVinoYoloV5Detector
# from lib.OpenVinoSSDLiteDetector import OpenVinoSSDLiteDetector


class Algorithm():
    def __init__(self,weights_path,params):
        print("__init__.%s"%(self.__class__.__name__))

        print("\t",weights_path,params)

        openVinoYoloV5Detector_IN_conf = {
            "weight_file": weights_path+"/yolov5n_openvino_model/yolov5n.xml",
            # "weight_file": weights_path+"/yolov5n.onnx",
            "device": "GPU"
        }
        self.openVinoYoloV5Detector = OpenVinoYoloV5Detector(IN_conf=openVinoYoloV5Detector_IN_conf)

        # openVinoSSDLiteDetector_IN_conf = {
        #     "weight_file": weights_path+"/ssdlite_mobilenet_v2/FP16/ssdlite_mobilenet_v2.xml",
        #     "device": "CPU"
        # }
        # self.openVinoSSDLiteDetector = OpenVinoSSDLiteDetector(IN_conf=openVinoSSDLiteDetector_IN_conf)

        self.count = 0
    def __del__(self):
        print("__del__.%s"%(self.__class__.__name__))

    def release(self):

        print("python.release")
        del self

    def objectDetect(self,image_type,image):
        """
        @param image_type:  0:image为numpy格式的图片, 1:image为base64编码的jpg图片
        @param image:
        @return:
        """
        self.count += 1
        # print("python.objectDetect: count=%d"%(self.count),type(image_type),image_type,type(image))

        if 1 == image_type:
            # 1 == image_type 则 image是str类型的 image_base64
            encoded_image_byte = base64.b64decode(image)
            image_array = np.frombuffer(encoded_image_byte, np.uint8)
            image = cv2.imdecode(image_array, cv2.COLOR_RGB2BGR) # opencv 解码

        detect_num, detect_data = self.openVinoYoloV5Detector.detect(image)
        # detect_num, detect_data = self.openVinoSSDLiteDetector.detect(image)

        # print("python.objectDetect:",type(image),image.shape,detect_num,detect_data,detect_msg)

        data = {
            "code": 1000,
            "msg": "success",
            "result": {
                "detect_num": detect_num,
                "detect_data": detect_data
            }
        }
        return json.dumps(data,ensure_ascii=False)


    def __checkWeightFile(self,weight_file):
        if not os.path.exists(weight_file):
            e = "weight_file=%s not found"%weight_file
            raise Exception(e)



if __name__ == '__main__':
    import time
    weights_path = "weights"
    params = {

    }
    algorithm = Algorithm(weights_path=weights_path,params=params)


    url = 0
    # url = "F:\\file\\data\\zm-main.mp4"
    url = "F:\\file\\data\\camera.avi"

    cap = cv2.VideoCapture(url)

    while True:
        r, frame = cap.read()
        if r:
            scale = 1280 / max(frame.shape)
            if scale < 1:
                frame = cv2.resize(
                    src=frame,
                    dsize=None,
                    fx=scale,
                    fy=scale,
                    interpolation=cv2.INTER_AREA,
                )

            t1 = time.time()
            result = algorithm.objectDetect(image_type=0,image=frame)
            t2 = time.time()
            print("algorithm.objectDetect spend %.3f (s)"%(t2 - t1), result)
        else:
            print("读取%s结束" % str(url))
            break

    cap.release()
    cv2.destroyAllWindows()

