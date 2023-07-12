import requests
import time
import base64
import cv2

def objectDetect(filename):
    t1 = time.time()
    image = cv2.imread(filename)

    encoded_image_byte = cv2.imencode(".jpg", image)[1].tobytes()  # bytes类型
    image_base64 = base64.b64encode(encoded_image_byte)
    image_base64 = image_base64.decode("utf-8")  # str类型

    url = '%s/image/objectDetect'%backend_host
    params = {
        "appKey": appKey,
        "image_base64":image_base64,
        # "algorithm": "hm_detector_v1",
        # "algorithm": "hmk_detector_v1",
        "algorithm": "yolo_v5",
    }

    print("请求参数：url=%s,params.algorithm=%s"%(url,params.get("algorithm")))

    res=requests.post(url,data=params)
    t2 = time.time()
    t = "spend %.5f 秒"%(t2 - t1)
    # print(t,res.status_code,res.content)
    print(t,res.status_code,res.json())


    # cv2.imshow('image', image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
if __name__ == '__main__':

    appKey = "s84dsd#7hf34r3jsk@fs$d#$dd"
    backend_host = "http://127.0.0.1:9003"
    # backend_host = "http://127.0.0.1:9090"

    filename = "D:\\file\\data\\images\\1.jpg"


    objectDetect(filename)




