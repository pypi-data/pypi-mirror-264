import datetime
from django.db import models
from django.utils import timezone
from django.contrib import admin


# 应用名_类名生产的消协数据表名
class Question(models.Model):

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

    def __str__(self):
        return self.question_text

    @admin.display(
        boolean=True,
        ordering="pub_date",
        description="Published recently?",
    )
    # 之前1天内的日期返回Ture
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now


class Choice(models.Model):
    # 如果模型具有ForeignKey，则外键模型的实例将可以访问返回第一个模型的所有实例的管理器。
    # 默认情况下，此管理器的名称为Choice_set，其中Choice是源模型名称，小写。此管理器返回QuerySets，可以按照上面“检索对象”一节中的描述对其进行过滤和操作
    # 可以使用Foreign_key中的'related_name‘参数更改此单词(choice_set)。
    # question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="choices")
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
