from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.utils.safestring import mark_safe
import ollama
import textile
from .form import SignUpForm, LoginForm

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
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()          
            login(request['csrfmiddlewaretoken'], user)        
            return redirect('/.') 
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def login(request):
    username = ''
    password = ''
    secretcode = ''
    form = LoginForm(data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data['name']
            password = form.cleaned_data['password']
            secretcode = form.cleaned_data['code']
            user = authenticate(username=username, password=password, code=secretcode)
            
            if user is not None:
                login(request, user) 
                    
                return redirect('home')  
    redirect('/./profile')
    return render(request, 'profile.html', {'name': username})

def profile(request):
    return render(request, 'profile.html')