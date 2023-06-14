# SeSAC 파이널 프로젝트

<img width="815" height = "400" alt="스크린샷 2023-06-10 오후 3 41 58" src="https://github.com/Youth787/SESAC-FINAL/assets/90955152/d9e4b141-8e7d-4eaf-afaf-11dd98eaa4e3">

## Anyticon

개발 기간 : 2023.04.06 ~ 2023.05.24 (48일)

주제 : Anyone makes emoticon! AnyTicon.

비지니스 시사점 
- 개인화된 이모티콘을 제작하는 서비스 제공
- 이모티콘 제작을 자동화하고 사용자가 간편하게 이용할 수 있는 플랫폼을 구축하여 서비스를 제공하는 비지니스 모델 

시장성 
- 감정이나 의도를 더욱 효과적으로 전달 가능
- 개인화와 창의성의 시대에 사용자에게 독특하고 개성적인 표현 방식 제공
- SNS와 메신저를 사용하는 많은 사라마들이 이모티콘을 사용하고 있으므로, 다양한 사용자들에게 시장을 확장할 수 있는 잠재력 

## 팀원 
<img width="815" height = "400" alt="스크린샷 2023-06-10 오후 3 42 12" src="https://github.com/Youth787/SESAC-FINAL/assets/90955152/cb3bc5ba-0498-42d1-bd6d-01da8b18fd1e">

## 프로젝트 개요
<img width="815" height = "400"  alt="스크린샷 2023-06-10 오후 3 42 23" src="https://github.com/Youth787/SESAC-FINAL/assets/90955152/9fde871b-d943-48fe-a795-a1995d77de6d">

## Stacks 

### Language
<img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white"> 

### Front-end
<img src="https://img.shields.io/badge/html5-E34F26?style=for-the-badge&logo=html5&logoColor=white"> <img src="https://img.shields.io/badge/css-1572B6?style=for-the-badge&logo=css3&logoColor=white"> <img src="https://img.shields.io/badge/javascript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black"> <img src="https://img.shields.io/badge/webflow-4353FF?style=for-the-badge&logo=webflow&logoColor=black">

### Back-end
<img src="https://img.shields.io/badge/django-092E20?style=for-the-badge&logo=django&logoColor=white"> <img src="https://img.shields.io/badge/amazonec2-FF9900?style=for-the-badge&logo=amazonec2&logoColor=white"> <img src="https://img.shields.io/badge/ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white"> 

### Libarary
<img src="https://img.shields.io/badge/numpy-013243?style=for-the-badge&logo=numpy&logoColor=white"> <img src="https://img.shields.io/badge/pandas-150458?style=for-the-badge&logo=pandas&logoColor=white"> <img src="https://img.shields.io/badge/tensorflow-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white"> <img src="https://img.shields.io/badge/pytorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white"> <img src="https://img.shields.io/badge/opencv-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white">

### Environment
<img src="https://img.shields.io/badge/github-181717?style=for-the-badge&logo=github&logoColor=white"> <img src="https://img.shields.io/badge/git-F05032?style=for-the-badge&logo=git&logoColor=white"> <img src="https://img.shields.io/badge/gitlfs-F64935?style=for-the-badge&logo=gitlfs&logoColor=white"> <img src="https://img.shields.io/badge/visualstudiocode-007ACC?style=for-the-badge&logo=visualstudiocode&logoColor=white"> 

## 시작 가이드
**Requirements**
For building and running the application you need : 

    Django==3.2.4
    torch==1.11.0 
    torchvision==0.12.0
    transformers==4.11.3

## 데이터 셋

### Klue-bert
  - ai hub : 감성 대화 말뭉치 \
  https://aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&aihubDataSe=realm&dataSetSn=86
  - ai hub : 한국어 감정 정보가 포함된 단발성 대화 데이터셋 \
  https://aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100
  
### Stargan
  - 중앙대 연구, 이메일로 신청. \
  http://aihumanities.org/ko/archive/data/?vid=2
  - GAN 모델 github (pytorch 기반) \
  https://github.com/eriklindernoren/PyTorch-GAN

### Cyclegan 
  - 화풍 데이터 도메인인 지브리 이미지 데이터의 경우 지적 재산권이 会社スタジオジブリ에 있기 때문에 해당 결과물을 외부로 공개 또는 영리 목적으로 사용 금지. 전처리 소스코드 및 모델 구성 시 사용한 소스코드는 사용이 가능합니다. 화풍데이터가 아닌   실사 표정 이미지 도메인의 경우 AIHUB에서 구한 한국인 감정인식을 위한 복합영상 데이터가 출처입니다. 해당 자료 또한 내국인만 데이터 신청이 가능하여, 아래 첨부드리는 링크를 참고하여 사용조건을 확인해 주시면 감사하겠습니다. \
  https://aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&aihubDataSe=realm&dataSetSn=82



## 화면 구성 

<img width="815" height = "400" alt="스크린샷 2023-06-10 오후 3 42 38" src="https://github.com/Youth787/SESAC-FINAL/assets/90955152/c0936b64-9584-439d-b052-dfddbc53cb42">
<img width="815" height = "400" alt="스크린샷 2023-06-10 오후 3 42 45" src="https://github.com/Youth787/SESAC-FINAL/assets/90955152/80d3b974-f189-4100-8c62-bc3d52ed77f4">
<img width="815" height = "400" alt="스크린샷 2023-06-10 오후 3 42 53" src="https://github.com/Youth787/SESAC-FINAL/assets/90955152/72435593-5a5c-443e-adfa-1e809b4797e6">
<img width="815" height = "400" alt="스크린샷 2023-06-10 오후 3 43 01" src="https://github.com/Youth787/SESAC-FINAL/assets/90955152/dc7402e6-04d8-4771-a0bb-0640b5395a4d">
<img width="815" height = "400" alt="스크린샷 2023-06-10 오후 3 43 10" src="https://github.com/Youth787/SESAC-FINAL/assets/90955152/a9ff95fc-79bf-4e79-adc0-5fa1f042b99c">


