# 오요앱 (오늘의 요리 앱)


![oyoapp_project02](https://github.com/OyoMaster/aws-oyo-app/assets/158253607/54b9df3d-e077-4bb5-a289-61ea78457efd)


### 📅 기간
2024-01-16 ~ 2024-02-16 (총 32일)

### 📢 목적
고물가 & 고금리시대 부담스러운 외식 비용을 줄일 수 있도록 AI로 레시피 추천하는 서비스 

### 🍳 주요 기능
#### AI 상황별 레시피 추천
- 챗봇으로 맞춤별 쉬운 레시피 탐색
#### AI 냉장고 재료 레시피 추천
- 챗봇으로 남은 냉장고 재료로 만들 수 있는 레시피 추천
#### Youtube 레시피 영상 검색 기능
- 유튜브 검색으로 레시피 영상 탐색 가능




## 💫 프로젝트 소개

### 📌 작업순서

화면기획서 제작 > DB 테이블 설계 > API 설계 > API 개발 및 테스트 > 안드로이드 화면설계 > 안드로이드 개발 및 테스트

### 📎 관련 링크
화면 설계서 - https://www.figma.com/file/swR81qqaiqBZYNG9hfPP3O/1%EC%A1%B0-%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8-%ED%99%94%EB%A9%B4%EC%84%A4%EA%B3%84%EC%84%9C?type=design&node-id=0%3A1&mode=design&t=DDZ7FUwL5zIbNMeB-1

DB 테이블 명세서 - https://www.erdcloud.com/d/cgwCjQuiG2sPzYi7Q

API 명세서 - https://s-organization-242.gitbook.io/oyo-api/

프로젝트 기술서 - https://docs.google.com/presentation/d/1rBFHgJC2BXzM8MH8bK9H57ZY3D7s6R6PA1rkAUBNl_I/edit#slide=id.g2698337bf8e_0_9

### 📚 Stacks

<img src="https://img.shields.io/badge/flask-000000?style=for-the-badge&logo=flask&logoColor=white"> <img src="https://img.shields.io/badge/mysql-4479A1?style=for-the-badge&logo=mysql&logoColor=white"> <img src="https://img.shields.io/badge/serverless-FD5750?style=for-the-badge&logo=serverless&logoColor=white"> <img src="https://img.shields.io/badge/jsonwebtokens-000000?style=for-the-badge&logo=jsonwebtokens&logoColor=white">

<img src="https://img.shields.io/badge/awslambda-FF9900?style=for-the-badge&logo=awslambda&logoColor=black"> <img src="https://img.shields.io/badge/amazonrds-527FFF?style=for-the-badge&logo=amazonrds&logoColor=white"> <img src="https://img.shields.io/badge/amazons3-569A31?style=for-the-badge&logo=amazons3&logoColor=white"> <img src="https://img.shields.io/badge/docker-2496ED?style=for-the-badge&logo=docker&logoColor=white"> 

<img src="https://img.shields.io/badge/git-F05032?style=for-the-badge&logo=git&logoColor=white">

### 🎇 Architecture

![image](https://github.com/OyoMaster/oyo-app-api/assets/158253607/f6d0c5de-4520-484a-bd80-9ab083c76d6a)


### 🛠️ 작업 설명
MySQL을 이용한 관계형 데이터베이스(RDBMS)

빠르고 정확한 데이터 검색을 위한 Index설정

데이터의 효율적이고 유기적인 관리를 위한 왜래키(Foreign keys)에서의 cascade를 설정

Flask 프레임워크를 활용한  RestFul API 개발

JWT을 활용한 사용자 인증 및 권한 부여 구현

Passlib 라이브러리를 사용하여 비밀번호 암호화 및 이미일 형식 체크

Open API활용 (ChatGPT, 유튜브 검색, 카카오/구글 로그인)

---

Github의 Actions를 통한 애자일 방식의 배포 자동화(CI/CD)

AWS Lambda 함수로 RDS, S3 쿼리를 수행하여 Serverless 아키텍처 구축

개발환경의 일관성 유지를 위한 ECR 컨테이너 처리와 배포

ECR의 이미지 패키징을 위한 Docker 사용

AWS CloudWatch로 어플리케이션 모니터링 및 로그 파악하여 에러 해결





