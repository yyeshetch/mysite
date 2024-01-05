from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Choice, Question

def index(request):
	latest_question_list = Question.objects.order_by("-pub_date")[:5]
	# template = loader.get_template("polls/index.html")
	context = {
		"latest_question_list": latest_question_list
	}
	# return HttpResponse(template.render(context, request))
	return render(request, "polls/index.html", context)

# Output View
def detail(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	context = {
		"question": question
	}
	return render(request, "polls/detail.html", context)

def results(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	return render(request, "polls/results.html", {"question": question})

class IndexView(generic.ListView):
    template_name = "polls/index.html"
    # Model name by default for this listview will be question_list, to alter pass context_object_name
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by("-pub_date")[:5]

class DetailView(generic.DetailView):
	# A generic view should be pointed to model
	# by default it uses format app_name/model_name_detail.html, to alter pass template_name
    model = Question
    template_name = "polls/detail.html"

class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

# Processing View for "detail" output view
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
				"error_message": "You didn't select a choice."
			})
	else:
		selected_choice.votes += 1
		selected_choice.save()
		return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
