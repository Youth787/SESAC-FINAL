# 라이브러리 불러오기
from tensorflow.keras.models import load_model
import random
from tensorflow.keras.initializers import RandomNormal
import tensorflow as tf
import os
import numpy as np
import tensorflow_addons as tfa
import PIL
import cv2
import sys
from django.conf import settings


predicted_label = sys.argv[1]

#config
path = 'serving'
#haar, inputimage
source_folder = 'static'
destination_folder = 'static/stargan/outputs'
output_path = 'static/cyclegan/output.jpg'


# 최신 모델 선택하기
def latest_model(path):
    latest = os.listdir(path)
    latest.sort(reverse=True)  # 파일 이름을 정렬하여 최신 파일 선택
    string_model = latest[2][:-3]
    numofmodel = string_model[-3:]
    return numofmodel


# 모델 경로 불러오기
numofmodel = latest_model(path)

# 모델 불러오기
monet_generator = load_model('serving/monet_generator_002.h5', compile=False)
photo_generator = load_model('serving/photo_generator_002.h5', compile=False)
# monet_discriminator = load_model('./monet_discriminator_002.h5', compile=False)
# photo_discriminator = load_model('./photo_discriminator_002.h5', compile=False)


# frontalface cascade를 불러와 얼굴 디텍션
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# 소스 폴더에 있는 모든 파일 대상으로 크롭 진행
def haar(source_folder):
    for filename in os.listdir(source_folder):
        file_path = os.path.join(source_folder, filename)
        img = cv2.imread(file_path)
        faces = face_cascade.detectMultiScale(img, 1.2, 5)
        
        for i, (x,y,w,h) in enumerate(faces):
            face_crop = img[y:y+h, x:x+w]
            new_filename = os.path.join(destination_folder,f'{predicted_label}.jpg')
            cv2.imwrite(new_filename, face_crop)


# 이미지 로드
input_image_path = os.path.join('static/stargan/outputs',f'{predicted_label}.jpg')

# 이미지 전처리
input_image = PIL.Image.open(input_image_path)
input_image = input_image.resize((128, 128))  # 모델의 입력 크기에 맞게 조정
input_image = np.array(input_image) / 127.5 - 1.0  # 이미지를 [-1, 1] 범위로 정규화

# 예측 수행
generated_image = monet_generator.predict(np.expand_dims(input_image, axis=0))

# 생성된 이미지 후처리
postprocessed_image = generated_image[0] * 0.5 + 0.5  # 이미지 스케일 재조정
postprocessed_image = (postprocessed_image * 255).astype(np.uint8)  # 이미지를 [0, 255] 범위로 변환

# 결과 이미지 저장 또는 출력
output_image = PIL.Image.fromarray(postprocessed_image)
output_image.save(output_path)