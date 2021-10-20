from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,Http404, HttpResponseRedirect
from django.views import View
from .models import Question,Choice
from django.urls import reverse

class indexView(View):
    def get(self,request):
        latest_question_list = Question.objects.order_by('-pub_date')
        context = {
            'latest_question_list': latest_question_list
        }
        return render(request, 'polls/index.html', context=context)
class detailView(View):
    def get(self,request,question_id):
        # try:
        #     question = Question.objects.get(pk=question_id)
        # except Question.DoesNotExist:
        #     raise Http404('Question Does Not Exist')
        question = get_object_or_404(Question,id=question_id)
        return render(request,'polls/detail.html',{'question':question})
def results(request, question_id):
    question = get_object_or_404(Question,pk=question_id)
    context = {
        'question': question
    }
    return render(request,'polls/results.html',context)

def vote(request, question_id):
    question = get_object_or_404(Question,pk=question_id)
    try :
        selected_choice = question.choice_set.get(pk = request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else :
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results',args=(question.id,)))
