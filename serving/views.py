from django.shortcuts import render
from transformers import BertForSequenceClassification, BertTokenizer
from django.conf import settings
import os ,io, cv2, subprocess, shutil, torch
from PIL import Image
from django.http import HttpResponse, JsonResponse



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


# 얼굴 크롭 함수
def haar_face_crop(image_folder_path, file_name):
    # file의 경로 설정
    file = f'{image_folder_path}/{file_name}' # 윈도우에서는 \, 맥에서는 / 

    # haar_cascade 불러오기
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    file = cv2.imread(file)
    # 얼굴 x,y,w,h 위치 추출, 리스트 형태
    faces = face_cascade.detectMultiScale(cv2.cvtColor(file, cv2.COLOR_BGR2GRAY), 1.2, 5)
    
    for i, (x,y,w,h) in enumerate(faces):
        file = file[y:y+h, x:x+w]
        file = cv2.resize(file, (128,128))
        # file이라는 이미지를 크롭 사이즈에 맞게 자르면서 이미지 128x128사이즈로 리사이즈
            
    # 저장할 때 cv2.imwrite로 저장하면서 bgr >> rgb형태로 변환 저장, 이미지의 상세 경로 필요
    crop_image_path = os.path.join(settings.BASE_DIR, 'static', 'stargan', 'input', 'image', file_name)
    
    # 파일 저장을 return
    return cv2.imwrite(crop_image_path, file)


def download_combined_image(request):
    predicted_label = request.session.get('predicted_label')

    # 이미지 파일들을 가져옵니다.
    image1_path = 'static/stargan/input/image/input_img.jpg'
    image2_path = f'static/stargan/outputs/{predicted_label}.jpg'
    image3_path = 'static/cyclegan/output.jpg'

    with open(image1_path, 'rb') as f:
        image1_data = f.read()
    with open(image2_path, 'rb') as f:
        image2_data = f.read()
    with open(image3_path, 'rb') as f:
        image3_data = f.read()

    # 이미지 데이터를 BytesIO에 넣습니다.
    image1 = Image.open(io.BytesIO(image1_data))
    image2 = Image.open(io.BytesIO(image2_data))
    image3 = Image.open(io.BytesIO(image3_data))

    # 이미지를 하나로 합칩니다.
    combined_image = Image.new('RGB', (image1.width, image1.height + image2.height + image3.height))
    combined_image.paste(image1, (0, 0))
    combined_image.paste(image2, (0, image1.height))
    combined_image.paste(image3, (0, image1.height + image2.height))

    # 다운로드 응답을 생성하여 사용자에게 제공합니다.
    response = HttpResponse(content_type='image/jpeg')
    response['Content-Disposition'] = 'attachment; filename="combined_image.jpg"'
    combined_image.save(response, 'JPEG')
    
    return response


def base(request):
    if request.method == 'POST':
        if request.POST.get('submit') == 'result_12':
            return result_12(request)
        elif request.POST.get('submit') == 'result_13':
            return result_13(request)
    return render(request, 'base.html')


def result_12(request):
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
    
    # 얼굴 크롭 진행
    haar_face_crop(input_save_path, file_name)
    
    prediction = predict_sentiment(input_text)

    labels = {0: 'happy', 1: 'sad', 2: 'angry'}
    predicted_label = labels[prediction]

    request.session['predicted_label'] = predicted_label

    # play.py 실행 >> StarGAN을 통한 표정 생성
    subprocess.run(['python3', 'serving/play.py'])
    
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
    
    # Cyclegan 모델 실행 
    subprocess.run(['python3', 'serving/ImProvedCycleGANPredict.py', predicted_label])
    
    # 이미지 URL 생성
    image_url_input = os.path.join('static/stargan/input/image','input_img.jpg')
    image_stargan_output = os.path.join('static/stargan/outputs',f'{predicted_label}.jpg')
    
    context = {
        'input_text': input_text,
        'predicted_label': predicted_label,
        'image_url_input': image_url_input,
        'image_stargan_output' : image_stargan_output,
    }
    
    return render(request, 'result_12.html', context)
    



def result_13(request):
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
    
    # 얼굴 크롭 진행
    haar_face_crop(input_save_path, file_name)
    
    prediction = predict_sentiment(input_text)

    labels = {0: 'happy', 1: 'sad', 2: 'angry'}
    predicted_label = labels[prediction]

    request.session['predicted_label'] = predicted_label

    # play.py 실행 >> StarGAN을 통한 표정 생성
    subprocess.run(['python3', 'serving/play.py'])
    
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
    
    # Cyclegan 모델 실행 
    subprocess.run(['python3', 'serving/ImProvedCycleGANPredict.py', predicted_label])
    
    
    # 이미지 URL 생성
    image_url_input = os.path.join('static/stargan/input/image','input_img.jpg')
    image_cyclegan_output = os.path.join('static/cyclegan','output.jpg')
    
    context = {
        'input_text': input_text,
        'predicted_label': predicted_label,
        'image_url_input': image_url_input,
        'image_cyclegan_output': image_cyclegan_output,
    }
    
    return render(request, 'result_13.html', context)
