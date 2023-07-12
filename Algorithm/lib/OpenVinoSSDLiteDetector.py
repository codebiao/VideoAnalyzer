import time
import cv2
import numpy as np
# openvino 2022.1.0 has requirement numpy<1.20,>=1.16.6
from openvino.runtime import Core  # the version of openvino >= 2022.1

# 预测
# https://tech.amikelive.com/node-718/what-object-categories-labels-are-in-coco-dataset/
classes = [
    "background", "person", "bicycle", "car", "motorcycle", "airplane", "bus", "train",
    "truck", "boat", "traffic light", "fire hydrant", "street sign", "stop sign",
    "parking meter", "bench", "bird", "cat", "dog", "horse", "sheep", "cow", "elephant",
    "bear", "zebra", "giraffe", "hat", "backpack", "umbrella", "shoe", "eye glasses",
    "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite",
    "baseball bat", "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle",
    "plate", "wine glass", "cup", "fork", "knife", "spoon", "bowl", "banana", "apple",
    "sandwich", "orange", "broccoli", "carrot", "hot dog", "pizza", "donut", "cake", "chair",
    "couch", "potted plant", "bed", "mirror", "dining table", "window", "desk", "toilet",
    "door", "tv", "laptop", "mouse", "remote", "keyboard", "cell phone", "microwave", "oven",
    "toaster", "sink", "refrigerator", "blender", "book", "clock", "vase", "scissors",
    "teddy bear", "hair drier", "toothbrush", "hair brush"
]


class OpenVinoSSDLiteDetector():
    def __init__(self,IN_conf):

        # openvino >= 2022.1
        ie_core = Core()
        model = ie_core.read_model(model=IN_conf.get("weight_file"))
        net = ie_core.compile_model(model=model, device_name=IN_conf.get("device"))
        # get input and output nodes
        input_layer = net.input(0)
        output_layer = net.output(0)

        self.Net = net
        # get input size
        height, width = list(input_layer.shape)[1:3]
        print(input_layer.any_name, output_layer.any_name)
        print(height, width)



        self.INPUT_HEIGHT = 300
        self.INPUT_WIDTH = 300

    def process_results(self,h,w,results,thresh=0.6):
        # size of the original frame

        # results is a tensor [1, 1, 100, 7]
        results = results.squeeze()
        boxes = []
        class_ids = []
        scores = []

        for _, class_id, score, xmin, ymin, xmax, ymax in results:
            if score >= 0.4:
                class_id = int(class_id)

                x1 = int(xmin * w)
                y1 = int(ymin * h)
                width = int((xmax - xmin) * w)
                height = int((ymax - ymin) * h)


                if 1==class_id: # person

                    if height >= width:
                        boxes.append(
                            (x1,y1,width,height)
                        )
                        class_ids.append(class_id)
                        scores.append(score)

                elif 1!=class_id:# 非person

                    boxes.append(
                        (x1, y1, width, height)
                    )
                    class_ids.append(class_id)
                    scores.append(score)


        # apply non-maximum suppression to get rid of many overlapping entities
        # see https://paperswithcode.com/method/non-maximum-suppression
        # this algorithm returns indices of objects to keep
        indices = cv2.dnn.NMSBoxes(
            # bboxes=boxes, scores=scores, score_threshold=thresh, nms_threshold=0.6
            bboxes=boxes, scores=scores, score_threshold=0.25, nms_threshold=0.45
        )

        result_class_ids = []
        result_scores = []
        result_boxes = []

        for index in indices:
            result_class_ids.append(class_ids[index])
            result_scores.append(scores[index])
            result_boxes.append(boxes[index])

        return result_class_ids, result_scores, result_boxes

    def detect(self,image):

        # resize image and change dims to fit neural network input
        input_img = cv2.resize(
            src=image, dsize=(self.INPUT_WIDTH,self.INPUT_HEIGHT), interpolation=cv2.INTER_AREA
        )
        input_img = input_img[np.newaxis, ...]

        # openvino >= 2022.1
        results = self.Net([input_img])
        results = results[self.Net.output(0)]

        h, w = image.shape[:2]
        class_ids, scores, boxes = self.process_results(h,w, results=results)

        detect_num = 0  # 检测目标数量
        detect_data = []  # 检测目标位置


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
                "score": round(float(score), 2)
            })
            detect_num += 1

        return detect_num,detect_data

if __name__ == '__main__':
    IN_conf = {
        "weight_file":"../weights/ssdlite_mobilenet_v2/FP16/ssdlite_mobilenet_v2.xml",
        "device":"GPU"
    }

    detector = OpenVinoSSDLiteDetector(IN_conf=IN_conf)

    ################################################

    url = 0
    # url = "D:\\file\\data\\MonitorCamera\\人脸与人数\\视频5-10分钟-141人次.mp4"
    # url = "../201-vision-monodepth/data/Coco Walking in Berkeley.mp4"
    # url = "https://github.com/intel-iot-devkit/sample-videos/blob/master/store-aisle-detection.mp4?raw=true"
    url = "D:\\file\\data\\zm-main.mp4"
    url = "D:\\file\\data\\camera.avi"
    # url = "F:\\file\\data\\Camera\\Human_attributes\\renyi.mp4"
    # url = "F:\\file\\data\\Camera\\Gaoqing\\xianjing.mp4"
    # url = "F:\\file\\data\\Camera\\Gaoqing\\damalu.mp4"
    # url = "F:\\file\\data\\Camera\\Gaoqing\\jinxinbeilu.mp4"
    # url = "F:\\file\\data\\Camera\\Face\\shipin.mp4"
    # url = "F:\\file\\data\\Camera\\Face\\jinmen.mp4"
    # url = "F:\\file\\data\\Camera\\foreign1.mp4"

    capture = cv2.VideoCapture(url)

    while True:
        r, frame = capture.read()
        if r:
            # grab the frame
            # if frame larger than full HD, reduce size to improve the performance
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
                for detect_item in detect_data:

                    score = detect_item.get("score")
                    location = detect_item.get("location")
                    class_name = detect_item.get("class_name") +"-"+ str(score)

                    x1, y1, x2,y2 = location.get("x1"), location.get("y1"), location.get("x2"), location.get("y2")
                    cv2.rectangle(frame, (x1,y1), (x2,y2), (0,255,0), 2)
                    cv2.putText(frame, class_name, (x1, y1 + 10), cv2.FONT_HERSHEY_SIMPLEX, .5,(255,255,255))

            cv2.imshow('OpenVinoSSDLiteDetector.py', frame)
            cv2.waitKey(1)

        else:
            print("读取%s结束" % str(url))
            break

    capture.release()
    cv2.destroyAllWindows()