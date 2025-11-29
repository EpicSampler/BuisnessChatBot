from django.shortcuts import render
import ollama
from decouple import config

model ='deepseek-v3.1:671b-cloud'

def get_resp(message):
    print('try to get response')
    response = ollama.chat(
        model = model,
        messages=[
            {'role': 'system', 'content': 'Ты - помощник в крупной IT-компании. К тебе могут обращаться как сотрудники компании, так и ее клиенты. Твоя задача - давать понятные всем инструкции по решению их проблем, используй сдержанный язык - без восклицаний, только официально-деловой стиль'},
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
        return render(request, 'index.html', context={'answer': r})
    return render(request, template_name='index.html')
