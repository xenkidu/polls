from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import Question, Choice
from .forms import QuestionForm, ChoiceForm


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


# @method_decorator(login_required, name='dispatch')
class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

@method_decorator(login_required, name='dispatch')
class AddPollView(generic.CreateView):
    template_name = 'polls/poll_form.html'

    def get(self, request, *args, **kwargs):
        q_form = QuestionForm(instance=Question())
        c_forms = [ChoiceForm(prefix=str(x), instance=Choice()) for x in range(4)]
        return render(request, self.template_name, {'q_form': q_form, 'c_forms': c_forms})

    def post(self, request):
        q_form = QuestionForm(request.POST, instance=Question())
        c_forms = [ChoiceForm(request.POST, prefix=str(x), instance=Choice()) for x in range(4)]
        if q_form.is_valid() and all([cf.is_valid() for cf in c_forms]):
            question = q_form.save(commit=False)
            question.author = request.user
            question.save()
            for choice_form in c_forms:
                choice = choice_form.save(commit=False)
                choice.question = question
                choice.author = request.user
                choice.save()

            messages.success(request, f'Poll Added!')
            return redirect('polls:home')
        return render(request, self.template_name, {'q_form': q_form, 'c_forms': c_forms})


def vote_view(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

