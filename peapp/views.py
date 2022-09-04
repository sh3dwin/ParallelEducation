from email import contentmanager
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Max, Count
from .models import ExamResult, Favourite, MultipleChoiceQuestion, TextQuestion, Topic, TrueFalseQuestion, User
from django.contrib.auth import logout, authenticate, login

# Create your views here.

def home(request):
    # Load the home page with topics
    topics = Topic.objects.all()
    user = request.user
    favourites = Favourite.objects.filter(user_id=user.id)
    context = {'user': user, 'topics': topics[:3], 'favourites': favourites[:3]}
    return render(request, 'peapp/home.html', context)

def topics(request):
    topics = Topic.objects.all()
    context = {'user': request.user, 'topics': topics}
    return render(request, 'peapp/topics.html', context)

def topic(request, topic_id):
    # Load a certain topic
    topic = get_object_or_404(Topic, pk=topic_id)
    # Check if the user has favourited the topic
    user = request.user
    if user.is_authenticated:
        # This will execute if the user favourites the page by pressing the favourite button
        favourite = Favourite.objects.filter(user_id=user.id).filter(topic_id=topic_id)
        if request.method == "POST":
            if "favourite" in request.POST:
                if not favourite:
                    favourite = Favourite(user=request.user, topic=topic)
                    favourite.save()
                    return redirect('topic', topic_id=topic_id)
                else:
                    favourite.delete()
                    return redirect('topic', topic_id=topic_id)
    else:
        favourite = None

    context = {'user': request.user, 'topic': topic, 'favourite': favourite}
    return render(request, 'peapp/topic.html', context)


def about(request):
    context = {'user': request.user}
    return render(request, 'peapp/about.html', context)


def exam(request, topic_id):
    # Load the exam for a topic
    topic = get_object_or_404(Topic, pk=topic_id)
    if request.method == 'POST':
        text_questions = TextQuestion.objects.filter(topic_id=topic.id)
        bool_questions = TrueFalseQuestion.objects.filter(topic_id=topic.id)
        multiple_choice_questions = MultipleChoiceQuestion.objects.filter(topic_id=topic.id)
        wrong=0
        correct=0
        total=0
        for q in bool_questions:
            total+=1
            if q.answer and  request.POST.get(q.question) == "True":
                correct+=1
            else:
                wrong+=1
        for q in multiple_choice_questions:
            total+=1
            if q.ans ==  request.POST.get(q.question):
                correct+=1
            else:
                wrong+=1
        for q in text_questions:
            total+=1
            if q.answer ==  request.POST.get(q.question):
                correct+=1
            else:
                wrong+=1
        
        context = {
            'topic' : topic,
            'correct':correct,
            'wrong':wrong,
            'total':total
        }
        if request.user.is_authenticated:
            result = ExamResult.objects.get(user = request.user, topic = topic)
            new_result = ExamResult(topic = topic, user = request.user, score = str(correct) + "/" + str(total))
            if not result or int(result.score.split('/')[0]) < correct:
                if result:
                    result.delete()
                new_result.save()
        return render(request, 'peapp/results.html', context)
    else:
        text_questions = TextQuestion.objects.filter(topic_id=topic_id)
        bool_questions = TrueFalseQuestion.objects.filter(topic_id=topic_id)
        multiple_choice_questions = MultipleChoiceQuestion.objects.filter(topic_id=topic_id)
        context = {
            'topic' : topic,
            'multiple_choice_questions': multiple_choice_questions,
            'bool_questions': bool_questions,
            'text_questions': text_questions
        }
        return render(request,'peapp/exam.html', context)

def results(request):
    # Load the result page for an exam
    return render(request, 'peapp/results.html')
    

def favourites(request):
    # Load the favourites tab
    user = request.user
    favourites = Favourite.objects.filter(user_id=user.id)
    context = {'user': user, 'favourites': favourites}
    return render(request, 'peapp/favourites.html', context)

def my_results(request):
    user = request.user
    topics = Topic.objects.all()
    results = ExamResult.objects.filter(user = user)
    print(results)
    context = {'user': user, 'results': results}
    return render(request, 'peapp/my_results.html', context)

def logout_view(request):
    logout(request)
    return render(request, 'peapp/logout.html')

def register_view(request):
    if request.method == "POST":
        username = request.POST.get("loginName")
        errorMessage = ""
        if User.objects.filter(username=username).exists():
            errorMessage = "Username already exist"
            return render(request, 'peapp/register.html', {'error': errorMessage})
        password = request.POST.get("loginPassword")
        conf_password = request.POST.get("loginConfirmPassword")
        if password != conf_password:
            errorMessage = "Passwords don't match"
            return render(request, 'peapp/register.html', {'error': errorMessage})
        user = User.objects.create_user(username=username, password=password)
        user.save()
        login(request, user)
        return redirect('home')
    return render(request, 'peapp/register.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("loginName")
        errorMessage = ""
        if not User.objects.filter(username=username).exists():
            errorMessage = "Username doesn't exist"
            return render(request, 'peapp/login.html', {'error': errorMessage})
        password = request.POST.get('loginPassword')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return redirect('home')
        else:
            errorMessage = "Incorrect password"
            # Return an 'invalid login' error message.
            return render(request, 'peapp/login.html', {'error': errorMessage})
    return render(request, 'peapp/login.html')    

