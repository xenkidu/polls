from django.http import HttpResponse

from django.shortcuts import render, get_object_or_404

from .models import Question


def index_view(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {
        'latest_question_list': latest_question_list,
    }
    return render(request, 'polls/index.html', context)


def detail_view(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


def results_view(request, question_id):
    response = f"You're looking at the results of question {question_id}"
    return HttpResponse(response)


def vote_view(request, question_id):
    return HttpResponse(f"You're voting on question {question_id}")


