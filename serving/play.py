import subprocess

command = [
    'python3',
    'serving/main.py',
    
    '--mode', 'test', # test가 학습 모델을 통해 구동하는 모드
    '--dataset', 'RaFD',
    '--rafd_crop_size', '128',  # 인풋 이미지 크롭 사이즈 128x128로 맞췄으니 무시해도 됨
    '--image_size', '128',      # 생성 이미지 크기, 인풋 이미지와 크기 맞춤
    '--c_dim', '3',             # 클래스 넘버에 맞추면 됨
    '--test_iters', '2000000',  # test할 때 몇 번째 가중치 파일을 사용할지
                                # 현재 200만번 돌린 모델
    
    # 여기서부터는 폴더 경로
    '--rafd_image_dir', 'stargan/input',   # 여기가 이미지 인풋 폴더
    '--sample_dir', 'stargan/outputs/samples',
    '--log_dir', 'stargan/outputs/logs',
    '--model_save_dir', 'stargan/outputs/models',
    '--result_dir', 'stargan/outputs/results' # 여기에 결과물 출력
    
]
subprocess.call(command) # 이게 py 호출 코드