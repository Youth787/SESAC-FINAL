window.addEventListener('DOMContentLoaded', function() {
    // save 버튼 클릭 이벤트 리스너 추가
    document.getElementById('save-btn').addEventListener('click', function() {
        // 예측된 라벨 값을 가져옵니다.
        var predictedLabelElement = document.getElementById('predicted-label');
        var predictedLabel = predictedLabelElement.innerText;

        // 이미지 처리 및 다운로드 응답을 생성하는 URL로 이동합니다.
        window.location.href = "/combined_image/?predicted_label=" + predictedLabel;
    });
});

$(document).ready(function() {
    // Submit 버튼 클릭 시 로딩 화면 표시
    $('form').submit(function() {
    $('#loading-screen').show();
    });

    // 로딩 화면에서 카운트다운 시작
    var secondsLeft = 35;
    var countdownInterval = setInterval(function() {
    secondsLeft--;
    $('#countdown').text(secondsLeft);
    if (secondsLeft === 0) {
        clearInterval(countdownInterval);
        window.location.href = '/result/';  // result 페이지로 이동
    }
    }, 1000);
});