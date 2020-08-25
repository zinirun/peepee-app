# peepee-app
Pee Analysis with OpenCV (Flask, Web)

## 피피 개발의 시작
### 인공지능 소변분석 웹서비스 프로젝트
서버 그룹 스터디를 마무리할 때쯤 학교측에서 서버를 제공해서 이용할 수 있을 때 많이 써먹어보고 싶어서 만들기로 한 것은 소변 색으로 건강을 분석해주는 프로그램. 한창 웹으로 뭔가를 서비스해보고 싶었는데 재미있겠다 싶었다. 나는 뭔가를 만들 때 이름부터 짓는다. 소변분석기...같은 식상한 이름보다는 Pee(소변)를 두번 말해서 은근히 귀여운 피피로 지어서 유저에게 거부감을 그나마 적게 주고 싶었다.

### 기술 스택
`HTML/CSS/JS` `Python` `Flask` `OpenCV` `Nginx` `Docker` `NHN Toast Cloud`

### 알고리즘
- 1. main.py에서 flask 기반의 웹을 구동하고 index.html으로 메인화면을 렌더링한다.
- 2. 메인화면에서 사진을 업로드하면 파이썬 라이브러리 opencv를 사용하여 이미지의 색상을 추출한다.
- 3. 픽셀 값을 기준으로 소변의 타입을 나눈다.
- 4. 소변의 타입을 result.html로 데이터와 함께 렌더링한다.
- + `Dockerfile`을 작성해서 도커로 배포도 쉽게 해보고 싶었다.

### 구현 전의 의문점
- 1. html이랑 python의 데이터(함수의 리턴값)를 어떻게 주고 받을건데?
- 2. 사진마다 소변 영역의 부분이 다를텐데 어떻게 맞출건데?
- 3. 소변 색상의 타입은 어떻게 나눌건데?

### 의문점에 대한 결론
- 1. json 타입의 데이터를 렌더링, 함수 호출 시 사용한다.
- 2. 사진의 중간 100px * 100px 부분만 추출하여 opencv 처리한다.
- 3. <a href="https://news.joins.com/article/21381482">"11가지 소변의 색으로 알아보는 내 건강상태"</a>라는 기사가 있다.


결국 핵심적인 코드는 opencv 처리와 이미지 rgb값마다 타입을 나누는 코드이다.

### 구현 완료 후 Dockerfile 작성하기
```dockerfile
FROM tiangolo/uwsgi-nginx-flask:python3.7
COPY ./app /app
RUN pip install -r requirements.txt
```
### Docker Service
```bash
docker build -t pp-app .
docker run -d --name pp-app -p 80:80 pp-app:latest
```
도커 이미지를 성공적으로 만들었고 호스트의 80포트와 도커의 80포트(nginx 프레임워크는 기본적으로 80포트 사용)를 연결하고 백그라운드로 실행한다.
