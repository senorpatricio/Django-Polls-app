# Here is the long way, importing the HttpResponse, Loader, and supplying a context 

# from django.http import HttpResponse, Http404, HttpResponseRedirect
# from django.template import loader
# from django.shortcuts import get_object_or_404, render
# from django.core.urlresolvers import reverse

# from .models import Choice, Question

# 
# these views are not using the generic views system.
# 

# def index(request):
# 	latest_question_list = Question.objects.order_by('-pub_date')[:5]
# 	template = loader.get_template('polls/index.html')
# 	context = {
# 		'latest_question_list': latest_question_list,
# 	}
# 	return HttpResponse(template.render(context, request))

# def detail(request, question_id):
#     try:
#         question = Question.objects.get(pk=question_id)
#     except Question.DoesNotExist:
#         raise Http404("Question does not exist")
#     return render(request, 'polls/detail.html', {'question': question})

# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {'question': question})


# def vote(request, question_id):
# 	question = get_object_or_404(Question, pk=question_id)
# 	try:
# 		selected_choice = question.choice_set.get(pk=request.POST['choice'])
# 	except (KeyError, Choice.DoesNotExist):
# 		# Redisplay the question voting form
# 		return render(request, 'polls/detail.html', {
# 			'question': question,
# 			'error_message': "You didn't select a choice.",
# 		})
# 	else:
# 		selected_choice.votes += 1
# 		selected_choice.save()
# 		# always return an HttpResponceRedirect after successfully dealing 
# 		# with POST data. this prevents data from being posted twice if the 
# 		# user hits the 'back' button
# 		return HttpResponseRedirect(reverse('polls:results', args=(question.id,))) 
# 		# 'reverse' is so you don't have to hardcode a URL in the view function
# 		# example: for question 34, result URL will be 'polls/34/results/'

# here's a shortcut using render, which will load the template, fill a context 
# and return an HttpResponse. does the same as the code above.

# from django.shortcuts import render

# from .models import Question


# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     context = {'latest_question_list': latest_question_list}
#     return render(request, 'polls/index.html', context)



# 
# 	Generic Views System
# 

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic

from .models import Choice, Question

class IndexView(generic.ListView):
	template_name = 'polls/index.html'
	context_object_name = 'latest_question_list'

	def get_queryset(self):
		""" Return the last five published questions """
		return Question.objects.order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
	model = Question
	template_name = 'polls/detail.html'

class ResultsView(generic.DetailView):
	model = Question
	template_name = 'polls/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
		# 'reverse' is so you don't have to hardcode a URL in the view function
		# example: for question 34, result URL will be 'polls/34/results/'