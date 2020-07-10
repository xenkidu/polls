from django.http import HttpResponse

from .models import Question

def index_view(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    output = ', '.join([q.question_text for q in latest_question_list])
    return HttpResponse(output)


def detail_view(request, question_id):
    return HttpResponse(f"You're looking at question {question_id}.")


def results_view(request, question_id):
    response = f"You're looking at the results of question {question_id}"
    return HttpResponse(response)


def vote_view(request, question_id):
    return HttpResponse(f"You're voting on question {question_id}")


