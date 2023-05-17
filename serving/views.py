from django.shortcuts import render
import torch
from transformers import BertForSequenceClassification, BertTokenizer
from django.conf import settings
from django.templatetags.static import static
import shutil
import os
import subprocess


# 모델과 토크나이저 로드
model_path = './bert_multi_sentiment.pt'
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = BertForSequenceClassification.from_pretrained('klue/bert-base', num_labels=3)
model.load_state_dict(torch.load(model_path, map_location=device))
model.to(device)
tokenizer = BertTokenizer.from_pretrained('klue/bert-base')

# 예측 함수
def predict_sentiment(input_text):
    inputs = tokenizer.encode_plus(input_text, add_special_tokens=True, truncation=True, max_length=64, padding='max_length', return_tensors='pt')
    input_ids = inputs['input_ids'].to(device)
    attention_mask = inputs['attention_mask'].to(device)
    
    with torch.no_grad():
        outputs = model(input_ids, attention_mask=attention_mask)
        logits = outputs.logits
        predicted_class = torch.argmax(logits, dim=1).item()
    
    return predicted_class

# Django 뷰

def main(request):
    if request.method == 'POST':
        input_text = request.POST.get('input_text', '')
        input_image = request.FILES.get('input_image')

        # 이미지 저장 경로 설정
        input_save_path = os.path.join(settings.BASE_DIR, 'static','stargan', 'input','image')

        # 이미지 저장
        file_name = 'input_img.jpg'
        if input_image:
            with open(os.path.join(input_save_path, file_name), 'wb') as f:
                for chunk in input_image.chunks():
                    f.write(chunk)
        
        prediction = predict_sentiment(input_text)

        labels = {0: 'happy', 1: 'sad', 2: 'angry'}
        predicted_label = labels[prediction]

        # play.py 실행 >> StarGAN을 통한 표정 생성
        subprocess.run(['python', 'serving/play.py'])
        
        # 파일 경로 설정
        results_save_path = os.path.join(settings.BASE_DIR, 'static', 'stargan','outputs','results')
        outputs_save_path = os.path.join(settings.BASE_DIR, 'static','stargan', 'outputs')
        src_image = os.path.join(results_save_path, f'{predicted_label}.jpg')
        des_image = os.path.join(outputs_save_path, f'{predicted_label}.jpg')
        # src_image = os.path.join('static/stargan/outputs/results', f'{predicted_label}.jpg')
        # des_image = os.path.join('static/stargan/outputs', f'{predicted_label}.jpg')
        
        # 파일 이동
        shutil.move(src_image, des_image)

        # stargan/results 폴더 내부 파일들 삭제
        folder_path = os.path.join(settings.BASE_DIR, 'static','stargan', 'outputs','results')
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
        # 추후 input_image와 stargan_output에 있는 파일도 삭제하게 만들 것
        
        # 이미지 URL 생성
        image_url_output = os.path.join('static/stargan/outputs',f'{predicted_label}.jpg')
        image_url_input = os.path.join('static/stargan/input/image','input_img.jpg')
        
        context = {
            'input_text': input_text,
            'predicted_label': predicted_label,
            'image_url_output': image_url_output,
            'image_url_input': image_url_input
        }
        
        return render(request, 'serving/result.html', context)
    return render(request, 'serving/main.html')











# from django.shortcuts import render
# import torch
# import requests
# from transformers import BertForSequenceClassification, BertTokenizer
# from transformers import pipeline

# model = None
# tokenizer = None

# def load_model():
#     global model, tokenizer
#     if model is None:
#         model = BertForSequenceClassification.from_pretrained('bert-base-uncased', force_download=True)
#         tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
#         state_dict = torch.load('./bert_multi_sentiment.pt', map_location=torch.device('cpu'))
        
#         state_dict['bert.embeddings.word_embeddings.weight'] = state_dict['bert.embeddings.word_embeddings.weight'][:30522, :]
#         state_dict['classifier.weight'] = state_dict['classifier.weight'][:2, :]
#         state_dict['classifier.bias'] = state_dict['classifier.bias'][:2]
        
#         model.load_state_dict(state_dict)
#         model.eval()

# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# def prediction(text):
#     global model, tokenizer
#     if model is None or tokenizer is None:
#         load_model()
#     label_dict = {0: '행복', 1: '슬픔', 2: '분노'}
#     encoded_text = tokenizer.encode_plus(
#         text,
#         add_special_tokens=True,
#         max_length=512,
#         padding='max_length',
#         truncation=True,
#         return_tensors='pt'
#     )
#     input_ids = encoded_text['input_ids'].to(device)
#     attention_mask = encoded_text['attention_mask'].to(device)
#     with torch.no_grad():
#         outputs = model(input_ids, attention_mask=attention_mask)
#         logits = outputs.logits
#         predicted_class = torch.argmax(logits, dim=1).item()
#     predicted_label = label_dict[predicted_class]
#     return predicted_label




# def main(request):
#     if request.method == 'POST':
#         input_text = request.POST.get('input_text', '')
#         predicted_result = prediction(input_text)
#         context = {'input_text': input_text,
#                    'predicted_label': predicted_result}
#         return render(request, 'serving/result.html', context)
#     return render(request, 'serving/main.html')







# def main(request):
#     load_model()

#     if request.method == 'POST':
#         input_text = request.POST.get('input_text', '')
#         tokens = tokenizer.encode_plus(
#             input_text,
#             max_length=64,
#             truncation=True,
#             padding='max_length',
#             add_special_tokens=True,
#             return_tensors='pt'
#         )
#         input_ids = tokens['input_ids']
#         attention_mask = tokens['attention_mask']

#         with torch.no_grad():
#             outputs = model(input_ids, attention_mask)
#             logits = outputs.logits
#             predicted_label = torch.argmax(logits, dim=1).item()

#         context = {
#             'input_text': input_text,
#             'predicted_label': predicted_label
#         }
#         return render(request, 'serving/result.html', context)

#     return render(request, 'serving/main.html')