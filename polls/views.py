from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404,HttpResponseRedirect
from .models import Question, Choice
from django.template import loader
from django.db.models import F
from django.urls import reverse
# Create your views here.

# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     template = loader.get_template("index.html")
#     context = {
#         'latest_question_list':latest_question_list
#     }
#     return HttpResponse(template.render(context,request))

def index(request):
    lastest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {
        "lastest_question_list" : lastest_question_list
    }
    return render(request, 'index.html',context)


def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        return HttpResponse("Your Question NOT exist!!!")
        # or raise Http404("Not exists!!")
    context = {
        "question" : question,
    }
    return render(request,"question_detail.html",context)
    # return HttpResponse("You're looking at question %s." %question_id)
    

# A shortcut: get_object_or_404()
# def Results
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "results.html", {"question": question})
# def results(request, question_id):
#     question = get_object_or_404(Question.objects.all(),pk=question_id)
#     context = {
#         "question" : question,
#     }
#     return render(request,"question_detail.html",context)
    # response = "You're looking at the results of questions %s."
    # return HttpResponse(response % question_id)

# votes
# def vote(request, question_id):
#     return HttpResponse("You're voting on question %s." % question_id)

def vote(request, question_id):
    
    question = get_object_or_404(Question, pk=question_id)
    
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except(KeyError, Choice.DoesNotExist):
        context = {'question': question, 'error_message':"You didn't select a choice " }
        return render(request, 'index.html',context)
    else:
        selected_choice.votes = F('votes') + 1
        selected_choice.save()
        
    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
