from django.shortcuts import render
from .models import *
from django.http import JsonResponse
# Create your views here.
from django.views.decorators.csrf import csrf_exempt

import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout



def home(request):
    courses = Course.objects.all()
    context = {'courses' : courses}
    return render(request , 'home.html' , context)
    

def api_question(request , id):
    raw_questions = Question.objects.filter(course =id)[:20]
    questions = []
    
    for raw_question in raw_questions:
        question = {}
        question['id'] = raw_question.id
        question['question'] = raw_question.question
        question['answer'] = raw_question.answer
        question['marks'] = raw_question.marks
        options = []
        options.append(raw_question.option_one)
        options.append(raw_question.option_two)
        if raw_question.option_three != '':
            options.append(raw_question.option_three)
        
        if raw_question.option_four != '':
            options.append(raw_question.option_four)
        
        question['options'] = options
         
        questions.append(question)
        
        
    return JsonResponse(questions , safe=False)
@login_required(login_url='/login')
def view_score(request):
    user = request.user
    score = ScoreBoard.objects.filter(user=user)
    context = {'score' : score}
    return render(request,'score.html' , context)

@login_required(login_url='/login')
def take_quiz(request , id):
    context = {'id' : id}
    return render(request , 'quiz.html'  , context)

@csrf_exempt
@login_required(login_url='/login')
def check_score(request):
    data = json.loads(request.body)
    user = request.user
    course_id = data.get('course_id')
    solutions = json.loads(data.get('data'))
    course = Course.objects.get(id=course_id)
    score = 0
    for solution in solutions:
        question = Question.objects.filter(id = solution.get('question_id')).first()
      
        if (question.answer) == solution.get('option'):
            score = score + question.marks
   
    score_board = ScoreBoard(course = course , score = score  , user = user)
    score_board.save() 
    
    return JsonResponse({'message' : 'success' , 'status':True})


