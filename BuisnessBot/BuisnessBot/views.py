from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.utils.safestring import mark_safe
import ollama
import textile
from .form import SignUpForm, LoginForm
from TelegramBot.models import Answers, Users, Organisations

model ='deepseek-v3.1:671b-cloud'

def get_resp(message):
    print('try to get response')
    response = ollama.chat(
        model = model,
        messages=[
            {'role': 'system', 'content': 'Ты - помощник в крупной IT-компании. К тебе могут обращаться как сотрудники компании, так и ее клиенты. Твоя задача - давать понятные всем инструкции по решению их проблем, используй сдержанный язык - без восклицаний, только официально-деловой стиль, пиши текст для пользователя с помощью MARKDOWN'},
            {'role': 'user', 'content': message}
        ],
        stream=False
    )
    answer = response['message']['content']

    Answers.objects.create(question=message, answer=answer)

    return answer

def answer(request):
    if 'question' in request.POST:
        a = request.POST['question']
        r = get_resp(a)
        ans = textile.textile(r)
        return render(request, 'index.html', context={'answer': mark_safe(ans)})
    return render(request, template_name='index.html')

def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'GET':
        form = SignUpForm(request.POST)
        if form.is_valid():

            s = Organisations()
            s.objects.create(name=request['name'], city=request['city'], director=request['2Name'] + request['Name'] + request['LastName'])   
            s.save() 

            user = form.save()          
            login(request['csrfmiddlewaretoken'], user)    
            return redirect('/.') 
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': request})

def login(request):
    form = LoginForm(data=request.GET or None)
    if request.method == 'GET':
        if form.is_valid():
            username = form.cleaned_data['2Name'] + form.cleaned_data['Name'] + form.cleaned_data['LastName']
            password = form.cleaned_data['Password']
            email = form.cleaned_data['Email']
            secretcode = form.cleaned_data['SecretCode']

            print(username, password, email, secretcode)

            s = Users()
            if s.objects.check(specialcode = secretcode, name = username, email = email) == True:
                user = authenticate(username=username, password=password, code=secretcode)
            else:
                return render(request, 'login.html', {'message': (username, password, email, secretcode)})
            
            if user is not None:
                login(request, user) 
                    
                return redirect('/./profile')  
    return render(request, 'login.html')

def profile(request):
    return render(request, 'profile.html')

def about(request):
    return render(request, 'about.html')