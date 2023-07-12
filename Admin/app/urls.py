
from django.urls import path
from .views.web import *
from .views.api import *


app_name = 'app'

urlpatterns = [

    path('', web_index),

    path('stream', web_stream),
    path('stream/play', web_stream_play),
    path('camera/add', web_camera_add),
    path('alarm', web_alarm),
    path('behavior', web_behavior),
    path('control', web_control),
    path('control/add', web_control_add),
    path('control/edit', web_control_edit),

    path('warning', web_warning),
    path('profile', web_profile),
    path('notification', web_notification),
    path('login', web_login),
    path('logout', web_logout),

    path('allCameraPushStream', api_allCameraPushStream),
    path('controlAdd', api_controlAdd),
    path('controlEdit', api_controlEdit),
    path('analyzerControlAdd', api_analyzerControlAdd),
    path('analyzerControlCancel', api_analyzerControlCancel),
    path('analyzerGetControls', api_analyzerGetControls),
    path('getIndex', api_getIndex),
    path('getStreams', api_getStreams),
    path('getVerifyCode', api_getVerifyCode)
]