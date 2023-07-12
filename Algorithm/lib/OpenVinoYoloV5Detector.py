import cv2
import numpy as np
import time

# openvino 2022.1.0 has requirement numpy<1.20,>=1.16.6
from openvino.runtime import Core  # the version of openvino >= 2022.1
from openvino.inference_engine import IECore # the version of openvino <= 2021.4.2


classes = ['person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light',
        'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
        'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee',
        'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard',
        'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
        'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch',
        'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
        'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear',
        'hair drier', 'toothbrush']  # class names

class OpenVinoYoloV5Detector():

    def __init__(self,IN_conf):

        # ie = Core()  # Initialize Core version>=2022.1
        # self.Net = ie.compile_model(model=IN_conf.get("weight_file"),device_name=IN_conf.get("device"))


        ie = IECore()  # Initialize IECore  openvino <= 2021.4.2
        self.Net = ie.load_network(network=IN_conf.get("weight_file"), device_name=IN_conf.get("device"))

        self.INPUT_HEIGHT = 640
        self.INPUT_WIDTH = 640

    # 按照YOLOv5 letterbox resize的要求，先将图像长:宽 = 1:1，多余部分填充黑边
    def image_fmt(self,image):
        row, col, _ = image.shape
        _max = max(col, row)

        image_fill = np.zeros((_max, _max, 3), np.uint8)
        image_fill[0:row, 0:col] = image

        return image_fill


    # YOLOv5的后处理函数，解析模型的输出
    def process_results(self,h,w,results,thresh=0.25):
        class_ids = []
        boxes = []
        scores = []

        results = results[0]
        rows = results.shape[0]

        y_factor = h / self.INPUT_HEIGHT
        x_factor = w / self.INPUT_WIDTH

        for r in range(rows):
            row = results[r]
            score = row[4]

            if score >= 0.4 :#default 0.4

                classes_scores = row[5:]

                _, _, _, max_indexes = cv2.minMaxLoc(classes_scores)
                class_id = max_indexes[1]

                if classes_scores[class_id] > 0.25:
                    x, y, w, h = row[0].item(), row[1].item(), row[2].item(), row[3].item()

                    x1 = int((x - 0.5 * w) * x_factor)
                    y1 = int((y - 0.5 * h) * y_factor)
                    width = int(w * x_factor)
                    height = int(h * y_factor)

                    boxes.append((x1,y1, width, height))

                    class_ids.append(class_id)
                    scores.append(score)


        # default score_threshold=0.25, nms_threshold=0.45
        indices = cv2.dnn.NMSBoxes(
            bboxes=boxes, scores=scores, score_threshold=thresh, nms_threshold=0.45
        )

        result_class_ids = []
        result_scores = []
        result_boxes = []

        for index in indices:
            result_class_ids.append(class_ids[index])
            result_scores.append(scores[index])
            result_boxes.append(boxes[index])

        return result_class_ids, result_scores, result_boxes

    def detect(self, image):

        detect_num = 0   # 检测目标数量
        detect_data = [] # 检测目标位置

        input_img = self.image_fmt(image)

        blob = cv2.dnn.blobFromImage(input_img, 1 / 255.0, (self.INPUT_WIDTH, self.INPUT_HEIGHT), swapRB=True,
                                     crop=False)

        # openvino >= 2022.1
        # results = net([blob])[next(iter(net.outputs))]
        # results = self.Net([blob])[self.Net.output(0)]

        # openvino <= 2021.4.2
        results = self.Net.infer(inputs={"images": blob})
        results = results["output"]


        h,w, _ = input_img.shape
        # h,w, _ = image.shape
        class_ids, scores, boxes = self.process_results(h, w, results)

        # 显示检测框bbox
        for (class_id, score, box) in zip(class_ids, scores, boxes):
            location = {
                "x1": box[0],
                "y1": box[1],
                "x2": box[0] + box[2],
                "y2": box[1] + box[3]
            }
            detect_data.append({
                "class_name": classes[class_id],
                "location": location,
                # "score": float("%.2f" % (float(confidence)))
                "score": round(float(score), 2)
            })
            detect_num += 1

        return detect_num,detect_data

if __name__ == '__main__':

    IN_conf = {
        # "weight_file":"../weights/yolov5m_openvino_model/yolov5m.xml",

        # "weight_file":"../weights/yolov5n-7-k5-256x320/yolov5n-7-k5_openvino_model/yolov5n-7-k5.xml",
        # "weight_file":"../weights/yolov5s_openvino_model/yolov5s.xml",
        # "weight_file":"../weights/yolov5n_openvino_model/yolov5n.xml",
        "weight_file": "../weights/yolov5n.onnx",
        "device":"GPU"
    }
    detector = OpenVinoYoloV5Detector(IN_conf=IN_conf)

    url = 0
    # url = "F:\\file\\data\\zm-main.mp4"
    url = "F:\\file\\data\\camera.avi"
    # url = "F:\\file\\data\\Camera\\Human_attributes\\renyi.mp4"
    # url = "F:\\file\\data\\Camera\\Gaoqing\\xianjing.mp4"
    # url = "F:\\file\\data\\Camera\\Gaoqing\\damalu.mp4"
    # url = "F:\\file\\data\\Camera\\Gaoqing\\jinxinbeilu.mp4"
    # url = "F:\\file\\data\\Camera\\Face\\shipin.mp4"
    # url = "F:\\file\\data\\Camera\\Face\\jinmen.mp4"
    url = "F:\\file\\data\\Camera\\foreign1.mp4"


    # cap = cv2.VideoCapture(url,cv2.CAP_DSHOW)
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
            detect_num, detect_data = detector.detect(frame)
            t2 = time.time()
            print("detect spend %.3f (s)"%(t2 - t1), detect_num, detect_data)

            if detect_num > 0:
                for dd in detect_data:

                    score = dd.get("score")
                    location = dd.get("location")
                    class_name = dd.get("class_name") +"-"+ str(score)

                    x1, y1, x2,y2 = location.get("x1"), location.get("y1"), location.get("x2"), location.get("y2")
                    cv2.rectangle(frame, (x1,y1), (x2,y2), (0,255,0), 2)
                    cv2.putText(frame, class_name, (x1, y1 + 20), cv2.FONT_HERSHEY_SIMPLEX, .5,(255,255,255))


            cv2.imshow('OpenVinoYoloV5Detector.py', frame)
            cv2.waitKey(1)


        else:
            print("读取%s结束" % str(url))
            break

    cap.release()
    cv2.destroyAllWindows()
