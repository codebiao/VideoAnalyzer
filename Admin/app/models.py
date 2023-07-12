from django.db import models
from django.utils import timezone


class Notification(models.Model):
    sort = models.IntegerField(verbose_name='排序')
    title = models.CharField(max_length=100, verbose_name='标题')
    content = models.CharField(max_length=200, verbose_name='内容')

    create_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    last_update_time = models.DateTimeField(auto_now_add=True,verbose_name='更新时间')

    state = models.IntegerField(verbose_name='状态') # 0 未读

    def __repr__(self):
        return self.title

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'av_notification'
        verbose_name = '通知'
        verbose_name_plural = '通知'


class Control(models.Model):
    user_id = models.IntegerField(verbose_name='用户')
    sort = models.IntegerField(verbose_name='排序')
    code = models.CharField(max_length=50, verbose_name='编号')

    stream_app = models.CharField(max_length=50, verbose_name='视频流应用')
    stream_name = models.CharField(max_length=100, verbose_name='视频流名称')
    stream_video = models.CharField(max_length=100, verbose_name='视频流视频')
    stream_audio = models.CharField(max_length=100, verbose_name='视频流音频')

    behavior_code = models.CharField(max_length=50, verbose_name='算法行为编号')
    interval = models.IntegerField(verbose_name='检测间隔')
    sensitivity = models.IntegerField(verbose_name='灵敏度')
    overlap_thresh = models.IntegerField(verbose_name='阈值')
    remark = models.CharField(max_length=200, verbose_name='备注')

    push_stream = models.BooleanField(verbose_name='是否推流')
    push_stream_app = models.CharField(max_length=50, null=True,verbose_name='推流应用')
    push_stream_name = models.CharField(max_length=100, null=True,verbose_name='推流名称')

    state = models.IntegerField(default=0,verbose_name="布控状态") # 0：未布控  1：布控中  5：布控中断

    create_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    last_update_time = models.DateTimeField(auto_now_add=True,verbose_name='更新时间')

    def __repr__(self):
        return self.code

    def __str__(self):
        return self.code

    class Meta:
        db_table = 'av_control'
        verbose_name = '布控'
        verbose_name_plural = '布控'

class Camera(models.Model):
    sort = models.IntegerField(verbose_name='排序')
    code = models.CharField(max_length=50, verbose_name='摄像头编号')
    name = models.CharField(max_length=100, verbose_name='摄像头名称')
    stream_name = models.CharField(max_length=200,verbose_name='视频流名称')
    stream_state = models.BooleanField(verbose_name='视频流状态')
    state = models.BooleanField(verbose_name='状态')
    remark = models.CharField(max_length=200, null=True, verbose_name='备注')
    create_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    last_update_time = models.DateTimeField(auto_now_add=True,verbose_name='更新时间')

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'av_camera'
        verbose_name = '摄像头'
        verbose_name_plural = '摄像头'