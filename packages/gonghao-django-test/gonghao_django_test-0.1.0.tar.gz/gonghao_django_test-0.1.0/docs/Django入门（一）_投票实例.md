# Django入门（1）

网址:

官网：[编写你的第一个 Django 应用，第 5 部分 | Django 文档 | Django (djangoproject.com)](https://docs.djangoproject.com/zh-hans/5.0/intro/tutorial05/)
W3CSchool：[Django4.0 开始-编写你的第一个Django应用，第5部分_w3cschool](https://www.w3cschool.cn/django4/django4-nwvu3lyt.html)

## Django

### 创建项目

- 安装

```
pip install django
```

- 创建项目（mtest）

```
django-admin startproject mtest
```

![](https://gitee.com/gonghao_git/draw-bed/raw/master/img/django%E9%86%92%E7%9B%AE%E6%96%B0%E5%BB%BA%E7%9B%AE%E5%BD%95%E7%BB%93%E6%9E%84-20240313221647918.png)

- 创建app文件（应用程序）

```
cd mtest
python ./manage.py startapp mtestapp
```

![image-20240313222812219](https://gitee.com/gonghao_git/draw-bed/raw/master/img/dj%E5%88%9B%E5%BB%BAapp%E7%A8%8B%E5%BA%8F-20240313222812219.png)

- 对比

<div style="display: flex;">     <img src="https://gitee.com/gonghao_git/draw-bed/raw/master/img/django%E9%86%92%E7%9B%AE%E6%96%B0%E5%BB%BA%E7%9B%AE%E5%BD%95%E7%BB%93%E6%9E%84-20240313221647918.png" style="width: 50%;">     <img src="https://gitee.com/gonghao_git/draw-bed/raw/master/img/dj%E5%88%9B%E5%BB%BAapp%E7%A8%8B%E5%BA%8F-20240313222812219.png" style="width: 50%;"> </div>



- 启动服务器端口测试

```
cd mtest
python .\mange.py runserver 127.0.0.1:8081
```



### 初始化页面

mtest

​	-- urls.py（注册路径）

mtestapp

​	--views.py（设置页面响应）

​	--urls.py（注册view）



1. 编辑views，开始就对应reqest给个HttpResponse返回值就行，def申明函数

2. urls.py引用包views,入参到path() > next/
3. 使用include包，include（"app.urls")  > n/

4. python mange.py runserver
5. 上述view,访问路径：ip:端口/next/n

> - 官网说明
>
> The `urlpatterns` list routes URLs to views. For more information please see:
>     https://docs.djangoproject.com/en/5.0/topics/http/urls/
>
> ```
> Function views
>     1. Add an import:  from my_app import views
>     2. Add a URL to urlpatterns:  path('', views.home, name='home')
> Class-based views
>     1. Add an import:  from other_app.views import Home
>     2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
> Including another URLconf
>     1. Import the include() function: from django.urls import include, path
>     2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
> ```



#### 返回静态页面

- 1. 根目录文件指定tempatles（若是设置DIRS随意点都行）目录，'APP_DIRS': True开启

  > 若mtest创建app项目文件夹polls，指定DIRS方式
  >
  > ![image-20240314234222700](https://gitee.com/gonghao_git/draw-bed/raw/master/img/setting%E4%B8%ADDIR%E6%96%87%E4%BB%B6%E6%8C%87%E5%AE%9A-20240314234222700.png)

- 2. 准备静态页面文件(/polls/tempates/list.html)

- views > from django.render  import render引入包

  ```
  def list(request):
      return render(request,"list.html")
  ```

  > 可以看出，此处指定函数list函数，在注册路径时引用绑定

- urls中绑定

  ```
  urlpatterns = [
      path("n/",views.shouye,name="index"),
      path("s/",views.list)
  ]
  ```

- 根目录文件下urls是否还需要注册？

  > path('one/',include("polls.urls"))个人理解这意思就是包含polls文件下的urls中所有的path，one为上层路径，那polls中urls注册的都是其下层的路径，所以无需注册了
  >
  > 直接访问IP：端口/one/s验证

- 静态页面用到的其他静态资源文件（img,js）
  1. polls(app文件夹)下创建文件夹static
  2. setting中设置STATIC_URL = 'static/'
  3. 注册INSTALLED_APPS可使用{% load static  %}



### 数据库连接

- 安装mysql组件

```
pip install mysqlclient
```

- 设置setting.py数据库信息

```
DATABASES = {
    'default': {
        #'ENGINE': 'django.db.backends.sqlite3',
        #'NAME': BASE_DIR / 'db.sqlite3',
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'dj',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',  # 如果 MySQL 服务器在本地
        'PORT': '3306',  # 默认 MySQL 端口
        'ATOMIC_REQUESTS': True, # 开启事务管理设置
    } 
}
```



### 表增删改

#### 增表

- INSTATLLED_APPS注册容器

```django
INSTALLED_APPS = [
    'django.contrib.admin',         #管理员站点
    'django.contrib.auth',          #认账授权系统
    'django.contrib.contenttypes',  #内容类型框架
    'django.contrib.sessions',      #会话框架
    'django.contrib.messages',      #消息框架
    'django.contrib.staticfiles',   #管理静态资源框架
    'polls.apps.PollsConfig',
]
```

- 编写模型（表）

  - app > models.py

  ```
  from django.db import models
  
  ## int,char,text,boolean,dataTime
  ## 外键，级联删除
  class table_name(models.Model):
  	l_nubmber = models.IntegerField
  	l2_name = models.CharField(max_length=100)
  	l3_description = models.TextField()
  	l4_is_active = models.BooleanField(default=True)
  	l5_created_at = models.DateTimeField(auto_now_add=True)
  	otherTable = models.ForeignKey(QiTaBiaoName, on_delete=models.CASCADE)
  ```

- 激活模型

```
python manage.py makemigrations
```

- 生成

```
python manage.py migrate
```



#### 增删改表中列

- 增加列

> model.py中添加和修改新的对象名，然后激活生成



### 数据增删改查

- **创建数据**：

```
# 创建新产品
new_product = table_name(l2_name='Sample Product', l3_description=‘l3’)
new_product.save()
```

- **查询数据**：

```
# 查询所有产品
products = Product.objects.all()

# 根据条件查询
product = Product.objects.get(l2_name='Sample Product')
```

- **更新数据**：

```
# 更新产品价格
product.l3_description =‘l3’
product.save()
```

- **删除数据**：

```
# 删除产品
product.delete()
```



### 创建用户

> 通过访问url/admin可访问默认登录界面，创建默认用户完成登录操作



- 创建用户

```
python manage.py createsuperuser
```

- 输入用户名和邮箱，重复输入密码创建

> Tips
>
> > 中文设置：LANGUAGE_CODE = 'zh-hans'
> >
> > ```
> > ### 组和用户。它们是由 django.contrib.auth 提供的
> > from django.contrib import admin
> > ```

### 页面显示自定义的models(库)

1. 从contrib中获取超级用户对象
2. 从Models中获取创建的表对象
3. 超级用户注册寄存表

```
from django.contrib import admin
from .models import Question
admin.site.register(Question)
```

- 设置后界面展示的表可正常增删改动

![image-20240320094039715](C:/Users/17364/AppData/Roaming/Typora/typora-user-images/image-20240320094039715.png)



### Get—From—URL

> - 询问12号问题
>
> URL/12
>
> - 询问12号问题答案页面(字符转代替) % id
>
> URL/12/result

- views.py,返回字符串，占位替代question_id

```pyhton
def detail(request, question_id):
    return HttpResponse("路径中的ID %s." % question_id)
```

- url.py ,设置路径,匹配路径调用函数

```python
urlpatterns = [
    # ex: /polls/5
    path("<int:question_id>/", views.detail, name="detail"),
]
```



#### 实例1

- 问题表按照日期所在列降序排序，先排序前5个

- 输出排序后的问题

> views.py

```python
def index(request):
    latest_question_str = Question.objects.order_by("-pub_date")[:5]
    output = ",".join([q.queation_text for q in latest_question_str])
    return HttpResponse(output)
```

> mkir  -r templates/polls
>
> touch index.html

>虽然我们现在可以将模板文件直接放在 `polls/templates` 文件夹中（而不是再建立一个 `polls` 子文件夹），但是这样做不太好。Django 将会选择第一个匹配的模板文件，如果你有一个模板文件正好和另一个应用中的某个模板文件重名，Django 没有办法 *区分* 它们。我们需要帮助 Django 选择正确的模板，最好的方法就是把他们放入各自的 *命名空间* 中，也就是把这些模板放入一个和 *自身* 应用重名的子文件夹里。

> views.py引用index.html模板  
>
> +++ from django.template import loader
>
> ​	++++ loader.get_templates.render()

```
def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    templates = loader.get_template("polls/index.html")
    #output = ",".join([q.question_text for q in latest_question_list])
    context = {"最新消息":latest_question_list}
    return HttpResponse(templates.render(context,request))
    #return HttpResponse(output)
```

- url创建url映射关系

```
path("",views.index,name="order")
```



> 快捷函数: render()

- from django.shortcuts import render

```
from django.shortcuts import render
from .models import Question
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)
```

- index.html

```
    {% if latest_question_list %}
    <ul>
        {% for question in latest_question_list %}
        <li><a href="/polls/{{ question.id }}/">{{ question.question_text }}</a></li>
        {% endfor %}
    </ul>
    {% else %}
    <p>No polls are available.</p>
    {% endif %}
```

- url.py

```
from django.urls import path
from . import views

urlpatterns = [
    path('t/', views.t_list),
    # ex: /polls/5
    path("<int:question_id>/", views.detail, name="detail"),
    # ex: /polls/5/results/
    path("<int:question_id>/results/", views.results, name="results"),
    # ex: /polls/5/vote/
    path("<int:question_id>/vote/", views.vote, name="vote"),
    path("",views.index,name="order")
]
```



### 硬编码的动态替换

- 我们访问地址/polls时跳转index页面，其中地址连接为硬编码
- {%url  'detail'  %}为url 中的name参数



### 命名空间的确认

> 硬编码的动态替换中，动态替换路径的方式是直接使用url的name,类似'detail'。
> 而在实际项目中，app有许多，为了避免重名，在name上层再添加一个标识，以app为单位归纳单元内所有Url,比如上述所有url都是polls的app下的操作，
>
> 那么我们命名这个单元的方式就是在url.py中标注

```
#app_name = 'polls'
```

- 而一旦命名成功，我们需要在原本仅使用Name引用的前提下，在name前添加空间名称,类似：

```
{% url 'polls:vote' %}
```

- 如果添加了命名空间而不使用空间前缀，那么很有可能报错

> <font color=red>500:error</font>

![image-20240326161358624](https://gitee.com/gonghao_git/draw-bed/raw/master/img/django%E5%91%BD%E5%90%8D%E7%A9%BA%E9%97%B4%E9%94%99%E8%AF%AF-20240326161358624.png)



### 投票系统完整实例

> 流程

1. 创建app启动和命名空间的确认

2. 主文件夹注册设置

3. view.py的请求响应逻辑编写

4. html页面动态的显示和跳转

5. urls.py匹配响应和跳转的url注册

#### 创建app启动和命名空间的确认

- 创建项目>实例pulls
- 命名空间（是否省略该步骤根据是否使用名称前缀调整）

```
app_name = 'polls'
```

#### 主文件夹注册设置

- 设置INSTALLED_APPS(app文件夹下app.py函数名为准)

```
'polls.apps.PollsConfig',
```

- DATABASES数据库
- TEMPLATES静态文件根目录

- LANGUAGE_CODE中文设置

#### 流程2~5

##### index(ip/polls)

![image-20240326165844892](C:/Users/17364/AppData/Roaming/Typora/typora-user-images/image-20240326165844892.png)

- 时间降序排序问题内容（“order_by("-pub_date")”）

> 包名:
> from .models import Question,Choice
>
> from django.template import loader
>
> from django.shortcuts import HttpResponse

```
def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    templates = loader.get_template("polls/index.html")
    #output = ",".join([q.question_text for q in latest_question_list])
    context = {"latest_question_list":latest_question_list}
    return HttpResponse(templates.render(context,request))
    #return HttpResponse(output)
```



- html（采用命名空间）

```
    {% if latest_question_list %}
    <ul>
        {% for question in latest_question_list %}
        <li><a href="{% url 'polls:detail' question.id %}">{{ question.question_text }}</a></li>
        {% endfor %}
    </ul>
    {% else %}
    <p>No polls are available.</p>
    {% endif %}
```

- urls

> from django.urls import path
>
> from . import views

```
 path("", views.index, name="index"),
```

##### detail(ip/polls/id)

![image-20240326165917820](https://gitee.com/gonghao_git/draw-bed/raw/master/img/details-20240326165917820.png)

- 编号问题和选择列表
- 查无编号404错误响应

> from django.shortcuts import get_object_or_404,render

```
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {"question": question})
```

- HTML

```
    <form action="{% url 'polls:vote' question.id %}" method="post">
        {% csrf_token %}
        <fieldset>
            <legend>
                <h1>{{ question.question_text }}</h1>
            </legend>
            {% if error_message %}<p><strong>{{ error_message }}</strong></p>{% endif %}
            {% for choice in question.choice_set.all %}
            <input type="radio" name="choice" id="choice{{ forloop.counter }}" value="{{ choice.id }}" onclick="printChoice(this)">
            <label for="choice{{ forloop.counter }}">{{ choice.choice_text }}</label><br>
            {% endfor %}
        </fieldset>
        <input type="submit" value="vote">
    </form>
    <script>
        function printChoice(radio){
            var choiceId = radio.id;
            console.log("choice ID:"  + choiceId)
        }
    </script>
```

- URLS

```
path("<int:question_id>/", views.detail, name="detail"),
```



##### vote(ip/polls/id/vote)



- 选择ID对应vote选中加 1保存
- 无编号情况错误响应

> from django.shortcuts import HttpResponseRedirect
>
> from django.urls import reverse
>
> from django.db.models import F

```
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes += 1
        selected_choice.save()

        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
```



- HTML

> 接受details页面投票请求，响应事件，响应跳转results页面



- URLs

```
 path("<int:question_id>/vote/", views.vote, name="vote"),
```



##### results.html

![image-20240326165950567](https://gitee.com/gonghao_git/draw-bed/raw/master/img/results-20240326165950567.png)

- 显示选择ID对应vote数量

```
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question": question})
```

- HTML 

```
    <h1>{{ question.question_text }}</h1>

    <ul>
        {% for choice in question.choice_set.all %}
        <li>{{ choice.choice_text }} -- {{ choice.votes }} vote{{ choice.votes|pluralize }}</li>
        {% endfor %}
    </ul>

    <a href="{% url 'polls:detail' question.id %}">Vote again?</a>
```

- URLs

```
path("<int:question_id>/results/", views.results, name="results"),
```



#### 精简实例

1. 转换 URLconf。
2. 删除一些旧的、不再需要的视图。
3. 基于 Django 的通用视图引入新的视图。

##### 改良 URLconf

```
 path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
```

##### 改良视图

```
class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"
```



### 测试教学

- 第一章第5部分



### 样式文件（静态文件加载实例）

- 美化页面样式引用css文件

- 关注settting文件设置中的STATIC_URL项“static/”（理论上语法应该是绝对路径“/staitc/”和相对路径“static/”）

- 创建polls/static/polls/style.css样式文件
- 同级创建polls/static/polls/images文件夹放置图片

- 页面引用样式方式

```
#预加载，文件开头处可加
{% load static %}

#头文件部分加载引用，static替换为项目路径下的static设置路径
<link rel="stylesheet" href="{% static 'polls/style.css'%}">

#背景图片引用
body{
    background: white url("images/bk.png") no-repeat;
}
```



### 主页和表格视图修改

#### 模板文件

- 实例模板（admin账号主页面）

  > base_site.html默认路径：
  >
  > Python\Python311\Lib\site-packages\django\contrib\admin\templates\admin\base_site.html
  >
  > ```
  > ## 修改文件中
  > {{ site_header|default:_('Django administration') }}
  > 
  > ## 替换为自定义内容可变更页面标题视图文字
  > Admin账号主页
  > ```
  >
  > ![image-20240327145336609](https://gitee.com/gonghao_git/draw-bed/raw/master/img/admin%E4%B8%BB%E9%A1%B5%E8%AF%95%E5%9B%BE%E4%BF%AE%E6%94%B9-20240327145336609.png)

- 项目文件修改

> 想要实现template模板修改，需要在manage.py同级主目录创建模板templates文件夹，修改setting.py中TEMPLATES参数项中DIRS属性默认值。
>
> - 创建templates/admin文件夹
>
> - 复制base_site.html文件到创建的admin文件夹下，代表该账号的模板文件
>
> - 设置中DIRS中添加扫描目录
>
>   ```
>   'DIRS': [BASE_DIR/'templates'],
>   ```
>
> - 自定义默认模板作为主页

### 表格视图修改

- 列举一些实例

1. 注册已有模型（数据库表格）
   - Queation,Choice为例

```
from django.contrib import admin
# Register your models here.
from .models import Question,Choice

admin.site.register(Question,QuestionAdmin)
admin.site.register(Choice)
```

![image-20240327150341668](https://gitee.com/gonghao_git/draw-bed/raw/master/img/%E6%B3%A8%E5%86%8C%E6%95%B0%E6%8D%AE%E5%BA%93%E8%A1%A8%E6%A0%BC-20240327150341668.png)

2. 列顺序修改

> 修改组内数据顺序即可
>
> ```
> list_display = ('question_text', 'pub_date', 'was_published_recently')
> ```
>
> ![](https://gitee.com/gonghao_git/draw-bed/raw/master/img/image-20240327151856765.png)



3. 外联表显示

> amdin.py中使用类即可

```
#admin.StackedInline	含字段名
#admin.TabularInline	隐藏字段名

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3
    
class QuestionAdmin(admin.ModelAdmin):
inlines = [ChoiceInline]
```

![image-20240327152916674](https://gitee.com/gonghao_git/draw-bed/raw/master/img/%E5%A4%96%E8%81%94%E8%A1%A8-20240327152916674.png)

4. display修饰器对表操作的应用

> 修改前
>
> ```
> class Question(models.Model):
>     question_text = models.CharField(max_length=200)  
>     pub_date = models.DateTimeField("date published")
>     def __str__(self):
>         return self.question_text
> ```
>
> 

![image-20240327151328625](https://gitee.com/gonghao_git/draw-bed/raw/master/img/%E4%B8%8D%E7%94%A8%E4%BF%AE%E9%A5%B0%E5%99%A8-20240327151328625.png)

> 修改后
>
> ```
> @admin.display(
>         boolean=True,
>         ordering='pub_date',
>         description='Published recently?',
>     )
>     def was_published_recently(self):
>         now = timezone.now()
>         return now - datetime.timedelta(days=1) <= self.pub_date <= now
> ```
>
> 

![image-20240327151610215](https://gitee.com/gonghao_git/draw-bed/raw/master/img/%E4%BF%AE%E9%A5%B0%E5%90%8E-20240327151610215.png)

- 过滤和搜索组件

> 条件框和搜索框
>
> ```
>    search_fields = ['question_text']
>    list_filter = ['pub_date']   
> ```
>
> 
>
> ![image-20240327152753057](https://gitee.com/gonghao_git/draw-bed/raw/master/img/%E6%90%9C%E7%B4%A2%E6%A1%86-20240327152753057.png)
>
> ![image-20240327152810677](https://gitee.com/gonghao_git/draw-bed/raw/master/img/%E8%BF%87%E6%BB%A4%E6%9D%A1%E4%BB%B6-20240327152810677.png)