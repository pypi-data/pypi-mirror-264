from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from .models import Question, Choice
from django.views import generic
from django.utils import timezone


class IndexView(generic.ListView):
    template_name = "t2020_polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        # return Question.objects.order_by("pub_date")[:3]

        # 返回一个查询集，其中包含pub_date小于或等于(即早于或等于)timezone.now的Questions
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("pub_date")[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = "t2020_polls/detail.html"

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

# class ResultsView(generic.DetailView):
#     model = Question
#     template_name = "t2020_polls/results.html"


def index(request):
    # 下述代码的作用是，载入 t2020_polls/index.html 模板文件，并且向它传递一个上下文(context)。
    # 这个上下文是一个 字典，它将模板内的变量映射为 Python 对象
    # -pub_date表示pub_date字段倒叙2个数据，pub_date表示正序2个数据
    latest_question_list = Question.objects.order_by("pub_date")[:2]

    # template = loader.get_template("t2020_polls/index.html")
    # context = {
    #     "latest_question_list": latest_question_list,
    # }
    # return HttpResponse(template.render(context, request))

    # 注意到，我们不再需要导入 loader 和 HttpResponse 。
    # 不过如果你还有其他函数（比如说 detail, results, 和 vote ）需要用到它的话，就需要保持 HttpResponse 的导入
    context = {"latest_question_list": latest_question_list}
    return render(request, "t2020_polls/index.html", context)


def detail(request, question_id):
    # return HttpResponse("You're looking at question %s." % question_id)
    # try:
    #     question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     # 界面: Page not found(404) 打印: Question does not exist
    #     raise Http404("Question does not exist")
    # return render(request, "t2020_polls/detail.html", {"question": question})
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "t2020_polls/detail.html", {"question": question})


def vote(request, question_id):
    # return HttpResponse("You're voting on question %s." % question_id)
    # https://docs.djangoproject.com/zh-hans/4.2/intro/tutorial04/
    # 拿到question表的所有属性
    question = get_object_or_404(Question, pk=question_id)
    try:
        # 拿到question的外键表的属性
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "t2020_polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        # t2020_polls>models.py的Choice类(表)变量(字段)操作
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.

        # HttpResponseRedirect 只接收一个参数：用户将要被重定向的 URL
        # HttpResponseRedirect 这不是 Django 的特殊要求，这是那些优秀网站在开发实践中形成的共识
        return HttpResponseRedirect(reverse("t2020_polls:results", args=(question.id,)))


def results(request, question_id):
    # response = "You're looking at the results of question %s."
    # return HttpResponse(response % question_id)
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "t2020_polls/results.html", {"question": question})
