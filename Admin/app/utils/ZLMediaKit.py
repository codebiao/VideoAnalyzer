import requests
import inspect

class ZLMediaKit():
    def __init__(self,mediaApiHost,mediaHttpHost,mediaRtmpHost):
        self.mediaApiHost = mediaApiHost
        self.secret = "035c73f7-bb6b-4889-a715-d9eb2d1925cc"
        self.default_push_stream_app = "analyzer"

        self.mediaHttpHost = mediaHttpHost
        self.mediaRtmpHost = mediaRtmpHost
        self.timeout = 3

    def __byteFormat(self,bytes, suffix="bps"):

        factor = 1024
        for unit in ["", "K", "M", "G"]:
            if bytes < factor:
                return f"{bytes:.2f}{unit}{suffix}"
            bytes /= factor

    def get_hlsUrl(self, app, name):

        return "%s/%s/%s.hls.m3u8" % (self.mediaHttpHost, app, name)

    def get_flvUrl(self, app, name):

        return "%s/%s/%s.live.flv" % (self.mediaHttpHost, app, name)

    def get_rtmpUrl(self, app,name):

        return "%s/%s/%s" % (self.mediaRtmpHost, app, name)



    def addStreamProxy(self,app,name,origin_url,vhost = "__defaultVhost__"):

        key = None # 添加成功返回的 "key" : "__defaultVhost__/proxy/0"  流的唯一标识

        try:
            url = "{host}/index/api/addStreamProxy?secret={secret}&vhost={vhost}&app={app}&stream={name}&url={origin_url}".format(
                host=self.mediaApiHost,
                secret=self.secret,
                vhost=vhost,
                app=app,
                name=name,
                origin_url=origin_url
            )

            res = requests.get(url, timeout=self.timeout)
            if res.status_code == 200:
                res_json = res.json()
                if 0 == res_json["code"]:
                    key = res_json["data"]["key"]

        except Exception as e:
            print("%s.%s error:%s"%(self.__class__.__name__,
                                    inspect.getframeinfo(inspect.currentframe().f_back)[2],
                                    str(e)))

        return key

    def delStreamProxy(self,key):

        flag = False # "flag" : true  成功与否
        try:
            url = "{host}/index/api/delStreamProxy?secret={secret}&key={key}".format(
                host=self.mediaApiHost,
                secret=self.secret,
                key=key
            )
            res = requests.get(url, timeout=self.timeout)
            if res.status_code == 200:
                res_json = res.json()
                if 0 == res_json["code"]:
                    if True == res_json["data"]["flag"]:
                        flag = True

        except Exception as e:
            print("%s.%s error:%s"%(self.__class__.__name__,
                                    inspect.getframeinfo(inspect.currentframe().f_back)[2],
                                    str(e)))

        return flag


    def getMediaList(self):
        __data = []
        try:
            url = "{host}/index/api/getMediaList?secret={secret}".format(
                host=self.mediaApiHost,
                secret=self.secret
            )
            res = requests.get(url,timeout=self.timeout)
            if res.status_code == 200:

                res_json = res.json()

                if 0 == res_json["code"]:
                    data = res_json["data"]
                    __data_group = {} # 视频流按照流名称进行分组
                    for d in data:
                        app = d.get("app")# 应用名
                        name = d.get("stream")# 流id
                        schema = d.get("schema")# 协议
                        code = "%s_%s"%(app,name)
                        v = __data_group.get(code)
                        if not v:
                            v = {}
                        v[schema] = d
                        __data_group[code] = v

                    for code,v in __data_group.items():
                        schemas_clients = []
                        index = 0
                        d = None
                        for __schema,__d in v.items():
                            schemas_clients.append({
                                "schema":__schema,
                                "readerCount":__d.get("readerCount")
                            })
                            if 0==index:
                                d = __d
                            index +=1

                        if d:
                            video_str = "无"
                            audio_str = "无"
                            tracks = d.get("tracks",None)
                            if tracks:
                                for track in tracks:
                                    codec_id = track.get("codec_id")
                                    codec_id_name = track.get("codec_id_name")
                                    codec_type = track.get("codec_type",-1)  # Video = 0, Audio = 1
                                    ready = track.get("ready")

                                    if 0==codec_type:
                                        fps = track.get("fps")
                                        height = track.get("height")
                                        width = track.get("width")

                                        video_str = "%s/%d/%dx%d" % (codec_id_name, fps,width, height)

                                    elif 1 == codec_type:
                                        channels = track.get("channels")

                                        sample_bit = track.get("sample_bit")
                                        sample_rate = track.get("sample_rate")

                                        audio_str = "%s/%d/%d/%d" % (
                                            codec_id_name, channels, sample_rate, sample_bit)

                            produce_speed = self.__byteFormat(d.get("bytesSpeed")) #数据产生速度，单位byte/s

                            app = d.get("app")  # 应用名
                            name = d.get("stream")  # 流id

                            __data.append({
                                "active":True,
                                "code":code,
                                "app":app,
                                "name":name,
                                "produce_speed":produce_speed,
                                "video":video_str,
                                "audio":audio_str,
                                "originUrl": d.get("originUrl"),  # 推流地址
                                "originType":d.get("originType"), # 推流地址采用的推流协议类型
                                "originTypeStr":d.get("originTypeStr"), # 推流地址采用的推流协议类型（字符串）
                                "clients": d.get("totalReaderCount"), # 客户端总数量
                                "schemas_clients":schemas_clients,
                                "flvUrl":self.get_flvUrl(app, name),
                                "hlsUrl":self.get_hlsUrl(app, name)
                                })

        except Exception as e:

            print("%s.%s error:%s"%(self.__class__.__name__,
                                    inspect.getframeinfo(inspect.currentframe().f_back)[2],
                                    str(e)))
        return __data