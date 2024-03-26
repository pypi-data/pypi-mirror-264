# Register your models here.
from django.contrib import admin

from .models import Question, Choice


# 创建一个模型后台类，调整字段展示
# class QuestionAdmin(admin.ModelAdmin):
#     # 字段
#     # fields = ["pub_date", "question_text"]
#     # 字段集
#     fieldsets = [
#         (None, {"fields": ["question_text"]}),
#         ("Date information2", {"fields": ["pub_date"]}),
#     ]
# 通过 admin.site.register(Question) 注册 Question 模型
# admin.site.register(Question, QuestionAdmin)
# admin.site.register(Choice)

# TabularInline 字段紧凑
class ChoiceInline(admin.TabularInline):
    model = Choice
    # 默认提供4个选项字段
    extra = 4


class QuestionAdmin(admin.ModelAdmin):
    # /admin/t2020_polls/question 展示数据字段或验证方法
    list_display = ["question_text", "pub_date", "was_published_recently"]
    # /admin/t2020_polls/question/1/change/具体哪个数据的详情页字段展示
    fieldsets = [
        (None, {"fields": ["question_text"]}),
        ("Date information", {"fields": ["pub_date"], "classes": ["collapse"]}),
    ]
    # 搜索栏,搜索 question_text
    search_fields = ["question_text"]
    # 设置边栏
    list_filter = ["pub_date"]
    # 关联外键属性
    inlines = [ChoiceInline]


# 注册两个表数据
admin.site.register(Question, QuestionAdmin)

