from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from django.views.generic import (
        ListView, 
        DetailView, 
        CreateView, 
        FormView
        )
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import Question, Choice, Comment
from .forms import QuestionForm, ChoiceForm, CommentForm


class IndexView(ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:10]


# @method_decorator(login_required, name='dispatch')
class DetailView(DetailView):
    model = Question


class ResultsView(DetailView):
    model = Question
    template_name = 'polls/results.html'
    form_class = CommentForm


    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a CommentForm
        form = self.form_class()
        context['form'] = form
        return context

    def post(self, request, *args, **kwargs):
        comment_form = CommentForm(request.POST, instance=Comment())
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.question = Question.objects.get(id=kwargs['pk'])
            comment.author = request.user
            comment.save()
            messages.success(request, f'Comment Added!')
            return redirect('polls:results', kwargs['pk'])
        return render(request, self.template_name)


@method_decorator(login_required, name='dispatch')
class PollCreateView(CreateView):
    template_name = 'polls/question_form.html'
    number_of_choices = 3

    def get(self, request, *args, **kwargs):
        q_form = QuestionForm(instance=Question())
        c_forms = [ChoiceForm(prefix=str(x), instance=Choice()) for x in range(self.number_of_choices)]
        return render(request, self.template_name, {'q_form': q_form, 'c_forms': c_forms})

    def post(self, request):
        q_form = QuestionForm(request.POST, instance=Question())
        c_forms = [ChoiceForm(request.POST, prefix=str(x), instance=Choice()) for x in range(self.number_of_choices)]
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
            return redirect('polls:detail', question.pk)
        return render(request, self.template_name, {'q_form': q_form, 'c_forms': c_forms})


def vote_view(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/question_detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

