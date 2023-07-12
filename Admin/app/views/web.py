from app.views.ViewsBase import *
from app.models import *
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from app.utils.Utils import validate_email, validate_tel,gen_random_code,gen_control_code


def web_index(request):
    context = {

    }


    return render(request, 'app/web_index.html', context)

def web_stream(request):
    context = {
    }

    # data = Camera.objects.all().order_by("-sort")

    return render(request, 'app/web_stream.html',context)

def web_camera_add(request):

    context = {
    }

    return render(request, 'app/web_camera_handle.html',context)


def web_stream_play(request):
    context = {
    }

    params = parse_get_params(request)

    app = params.get("app",None)
    name = params.get("name",None)

    url_true = False
    if app and name:
        url_true = True
        context["url"] = base_media.get_flvUrl(app, name)

    context["url_true"] = url_true

    return render(request, 'app/web_stream_play.html', context)

def web_alarm(request):
    context = {
    }
    context["data"] = [
        1,2,3,4
    ]

    return render(request, 'app/web_alarm.html', context)


def web_control(request):
    context = {
    }

    return render(request, 'app/web_control.html', context)

def web_control_add(request):
    context = {
    }

    context["streams"] = base_media.getMediaList()
    context["behaviors"] = base_behaviors
    context["handle"] = "add"
    context["control"] = {
        "code": gen_control_code(),
        "push_stream":False
    }

    return render(request, 'app/web_control_handle.html', context)

def web_control_edit(request):
    context = {
    }
    params = parse_get_params(request)

    code = params.get("code")
    control = None
    try:
        control = Control.objects.get(code=code)
    except:
        pass


    if control:

        # context["streams"] = media.getStreams()
        context["behaviors"] = base_behaviors
        context["handle"] = "edit"
        context["control"] = control

        context["control_stream_flvUrl"] = base_media.get_flvUrl(control.stream_app, control.stream_name)

        return render(request, 'app/web_control_handle.html', context)
    else:
        return redirect("/control")


def web_warning(request):
    context = {

    }
    return render(request, 'warning.html',context)

def web_notification(request):
    context = {

    }
    return render(request, 'notification.html', context)

def web_behavior(request):
    context = {

    }
    print(base_behaviors)
    context["data"] = base_behaviors




    return render(request, 'app/web_behavior.html', context)

def web_profile(request):
    context = {

    }
    return render(request, 'profile.html', context)

def web_logout(request):
    if request.session.has_key(base_session_key_user):
        del request.session[base_session_key_user]

    return redirect("/")


def web_login(request):
    context = {

    }

    if request.method == 'POST':
        code = 0
        msg = "error"

        params = parse_post_params(request)

        username = params.get("username")
        password = params.get("password")
        verify_code = params.get("verify_code")

        context["username"] = username
        context["password"] = password
        context["verify_code"] = verify_code

        session_verify_code = request.session.get("login_verify_code")
        if session_verify_code:
            if True or verify_code == session_verify_code:
                del request.session["login_verify_code"]

                if validate_email(username):
                    try:
                        user = User.objects.get(email=username)
                    except:
                        user = None
                    if not user:
                        msg = "邮箱未注册"
                elif validate_tel(username):
                    user = User.objects.get(username=username)
                    if not user:
                        msg = "手机号未注册"
                else:
                    user = User.objects.get(username=username)
                    if not user:
                        msg = "用户名未注册"
                if user:
                    if user.check_password(password):
                        if user.is_active:
                            user.last_login = datetime.now()
                            user.save()
                            request.session["user"] = {
                                "id": user.id,
                                "username": username,
                                "email": user.email,
                                "last_login": user.last_login.strftime("%Y-%m-%d %H:%M:%S")
                            }
                            code = 1000
                            msg = "登录成功"
                        else:
                            msg = "账号已禁用"
                    else:
                        msg = "密码错误"
            else:
                msg = "验证码错误"
        else:
            code = -10
            msg = "验证码已过期"

        res = {
            "code": code,
            "msg": msg
        }
        return HttpResponseJson(res)

    return render(request, 'app/web_login.html',context)