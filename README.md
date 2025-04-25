
# 프로젝트 설명

 주제 : AI를 활용한 사진 공감 서비스

 문제정의 : 칭찬과 위로가 줄어드는 사회는 사람들을 감정적 결핍으로 이끌 것이다.

 해결 방안 : 사용자가 최근 경험한 것이 담겨있는 '사진'에 접근하여 공감해주자.

 접근 방식 : 기존의 Image Captioning task에서는 사진에 대한 객관적인 설명만 존재하기 때문에, caption 텍스트를 칭찬, 공감 등의 목적으로 변환해주어 목적에 맞게 가공하였습니다.

 모델 비교 및 최종 모델 : 
 <Image Captioning>
     1. KoLLaVA(한국어 기반 이미지 멀티 모달 모델)
     2. BLIP Image-captioning
     3. expansionNet_v2(COCO Image-captioning SOTA)
  최종 모델 : BLIP Image-captioning

  모델 평가 방식 : 테스트 이미지에 대한 BLEU, ROUGE 점수 측정

  최종 웹 디자인 :
  <img width="397" alt="image" src="https://github.com/user-attachments/assets/befb6cbb-d16a-42ed-a922-6eb6476f774a" />

  
