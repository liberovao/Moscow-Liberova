from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from .models import Quest, Answer, Users
from django.urls import reverse
from django.contrib.auth import authenticate, login


def index(request):
    
    u = userdata(request)   
    if request.user.is_authenticated:
        latest_list = Quest.objects.order_by('quest_number')#[:5]  
        return render(request, 'DictIt/list.html', {"latest_list":latest_list, 'user_data':u})
    else:
        return render(request, 'index.html', )
    

def userdata(request):
    if request.user.is_authenticated:
        userid = int(request.user.id)
        try: 
            u = Users.objects.get(userid = userid)
        except:
            u = Users.objects.create(userid = userid, last_q = 0, trys = 0, r_answ = 0)
            u.save()
    else:
        u = 0
    return u

def updateuserdata(request, quest_id, ra):
    userid = int(request.user.id)
    u = Users.objects.get(userid = userid)
    if ra:
        u.r_answ = int(u.r_answ) + 1
    u.trys = int(u.trys) + 1
    u.last_q = quest_id
    u.save()
    

    
def lists(request):
    u = userdata(request)   
    if request.user.is_authenticated:
        latest_list = Quest.objects.order_by('quest_number')#[:5]  
        return render(request, 'DictIt/list.html', {"latest_list":latest_list, 'user_data':u})
    else:
        return render(request, 'index.html', )

def detail(request, quest_id):
    u = userdata(request)
    if request.user.is_authenticated:
        try:
            a = Quest.objects.get(quest_number = quest_id)
            b = Answer.objects.filter(quest_id = quest_id)
        
            #b = a.answer_set.all()
        except:
            raise Http404('Вопрос не найден')
        
        return render(request, 'DictIt/list/detail.html', {'question': a, 'answers': b, 'user_data':u})
    else:
        return render(request, 'index.html', )
def answer(request, quest_id):
    u = userdata(request)
    try:
        a = Quest.objects.get(quest_number = quest_id)
        ra  = a.quest_right_answ
    except:
        raise Http404('Вопрос не найден')
    
    try:
        ans = request.POST['ans']
    except:
        ref = ( reverse('DictIt:detail', args = (a.quest_number,)))
        return HttpResponseRedirect(ref)
        
    if  ans.strip().lower() == ra.strip().lower():
        #ref = ( reverse('DictIt:lists', args = ()))
        if (a.quest_number + 1 <= 24 ):
            ref = ( reverse('DictIt:detail', args = (a.quest_number + 1,)))
        else:
            ref = ( reverse('DictIt:lists', ))
        updateuserdata(request, quest_id, True)
    else:
        ref = ( reverse('DictIt:detail', args = (a.quest_number,)))
        updateuserdata(request, quest_id, False)
    return HttpResponseRedirect(ref)
    
    
def user_data(request):

    return render(request, 'DictIt/user_data.html', {'user_data':u})
    
