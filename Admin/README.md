#Admin 视频行为分析系统后台管理

#### 安装
| 程序         | 版本      |
| ---------- | ------- |
| python     | 3.7    |
| 依赖库      | requirements.txt |

#### 启动服务
~~~

# 创建虚拟环境
python -m venv venv

# 切换到虚拟环境
venv\Scripts\activate

# 更新虚拟环境的pip版本
python -m pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple

# 在虚拟环境中安装依赖库
python -m pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 在虚拟环境中启动服务
python manage.py runserver 0.0.0.0:9001

内置超级管理员用户：admin 密码：admin888

~~~

