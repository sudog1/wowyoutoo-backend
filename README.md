<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->


<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/sudog1/wowyoutoo-backend.git">
  <img src="https://github.com/sudog1/wowyoutoo-backend/issues/69#issue-2030045393" width="80" height="80">
  </a>

  <h3 align="center">WOW! YOU TOO?</h3>

  <p align="center">
    당신을 위한 AI 영어 선생님
    <br />
    <a href="https://github.com/sudog1/wowyoutoo-backend#readme"><strong>Explore the docs »</strong></a>
    <br />
    <br />
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

[![와너두](https://github.com/sudog1/wowyoutoo-backend/assets/89892255/2385e51e-ef2b-4c42-8c1e-b0537304fed8)
](https://wowyoutoo.me/main.html)

스픽, 산타토익 등 AI 를 이용한 언어학습이 상업적인 아이디어로 주목받고 있는 가운데, 저희는 이러한 사이트 중 '가볍게' 영어공부를 할 수 있는 사이트는 찾아볼 수 없다고 생각했습니다. 바쁜 현대 사회에서 길게 시간을 내어 영어공부를 하기란 큰 결심이 필요한 일이죠. 바로 그러한 이유로, 와!너두? 가 출시되었습니다.

### 와!너두? 는 이런 분들을 위해 만들어졌습니다.

* 틈틈히 영어공부를 하고 싶었지만 진짜 사람과 대화하기는 부담스러웠던 분들
* 긴 시간을 영어 공부에 할애하기 어려운 분들
* 기초적인 어휘부터 어려운 독해까지 한 번에 경험해보고 싶은 분들


## 주요 기능

- **회원 가입 / 로그인 / 소셜 로그인**
    
    ![로그인](https://github.com/sudog1/wowyoutoo-backend/assets/89892255/4a2fc70f-6286-4520-bde9-7658f9e1fc11)
    
    - 일반 회원가입은 이메일 인증을 통해 회원가입이 가능합니다.
    - 카카오와 깃허브 계정으로도 로그인이 가능합니다. 다만 이 경우에는 프로필 수정을 할 수 없습니다.
    
    
- **AI 채팅 기능**
    
   ![AI채팅](https://github.com/sudog1/wowyoutoo-backend/assets/89892255/8b7faee1-1001-4c44-85b4-dff4d90bc805)
    
    - gpt api 를 이용해 chat gpt 와 실시간 영어 채팅이 가능합니다.
    
- **영어 단어 문제**

    ![단어시험](https://github.com/sudog1/wowyoutoo-backend/assets/89892255/01cbfd18-9d67-48e4-b1b2-4fed3ad1f472)
    
    - 단어 데이터베이스에서 무작위로 10개를 가져와 단어 시험을 볼 수 있습니다.
    - 단어 데이터베이스는 총 1000개의 단어로 이루어져 있으며, 실용성 중심으로 배포된 파일을 이용하고 있습니다.
    - 틀렸거나, 맞았어도 잘 모르는 단어는 save 버튼을 통해 저장할 수 있습니다.
    
- **독해 지문 / 문제 생성 및 저장 기능**
  
    ![독해시험](https://github.com/sudog1/wowyoutoo-backend/assets/89892255/a7fc5e3e-b17b-4f40-afaa-fb32591ef113)
    
    - 로그인을 하지 않은 유저도 기존에 저장된 독해 지문에서 문제를 가져오는 기존 독해 지문 풀기가 가능합니다.
    - 로그인을 한 유저는 gpt 가 새롭게 생성해주는 지문을 일정 코인을 낸 뒤 풀고 저장할 수 있습니다.
    - 저장한 지문은 마이페이지에서 확인 가능하며, 내가 선택한 답과 정답을 보여줍니다.
    
- **영어 뉴스 제공 기능**
  
    ![뉴스페이지](https://github.com/sudog1/wowyoutoo-backend/assets/89892255/e990a73c-f9a3-4bf6-826c-a40adbe8ac5b)
    
    - NewYorkTimes api 를 이용해 만든 뉴스페이지 입니다. 기사의 내용을 대략적으로 볼 수 있고, 원한다면 클릭하여 해당 기사 링크로 이동할 수 있습니다.
    
- **마이페이지**
  
   ![마이페이지](https://github.com/sudog1/wowyoutoo-backend/assets/89892255/7c1d0f99-0672-4441-a3e3-a1a80eed2ac4)
   ![마이페이지_기능](https://github.com/sudog1/wowyoutoo-backend/assets/89892255/9a7924a8-fb72-4677-9c40-cccdc786946a)

  - 내 정보 수정 및 나의 정보를 열람할 수 있습니다.
  - 관리자라면 mypage 에서 백오피스로 들어갈 수 있습니다.
   
    
- **결제 기능**
    
  ![결제페이지](https://github.com/sudog1/wowyoutoo-backend/assets/89892255/f22d1c40-493a-4e70-a037-a921dbebccb5)

  - PortOne 을 통해 구현한 결제페이지입니다. 다양한 수단으로 결제할 수 있습니다.
 

- **백오피스**
  - 단체 이메일 보내기 / 공지사항 쓰기 / FAQ 답변하기 를 할 수 있습니다.
  - is_admin 이 true 일 시 마이페이지의 '백오피스' 버튼을 통해 들어올 수 있습니다.



<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

* [![VanillaJS][VanillaJS.com]][VanillaJS-url]
* [![Django][Django.com]][Django-url]
* [![CSS][CSS.com]][CSS-url]
* [![Python][Python.com]][Python-url]
* [![Celery][Celery.com]][Celery-url]
* [![Redis][Redis.com]][Redis-url]
* [![OpenAI][OpenAI.com]][OpenAI-url]
* [![Docker][Docker.com]][Docker-url]
* [![AmazonAWS][AmazonAWS.com]][AmazonAWS-url]
* [![Bootstrap][Bootstrap.com]][Bootstrap-url]
* [![JQuery][JQuery.com]][JQuery-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

크롬 브라우저 사용을 권장합니다.

### Prerequisites

requirements.txt 안의 라이브러리를 설치해주세요
* pip
  ```sh
  pip install -r requirements.txt
  ```

### Installation

API 키와 url 을 .env 파일에 담아주세요

1. 카카오 개발자 홈페이지에서 회원가입을 통해 API key 를 받아주세요 [https://developers.kakao.com/](https://developers.kakao.com/) github 는 settings 에서 발급받을 수 있습니다. 
[https://github.com/settings/developers](https://github.com/settings/developers) 에서 앱을 등록하고 키를 발급받아 주세요. 
OpenAI[https://platform.openai.com/account/api-keys](https://platform.openai.com/account/api-keys) 에서 회원가입을 한 뒤 api key 를 발급받아 주세요.
PortOne[https://portone.io/korea/ko](https://portone.io/korea/ko) 에서 회원가입을 한 뒤 시스템 설정 > 내정보의 API key, API secret을 설정하시고 "Get Token" 버튼을 통해 토큰을 발급받아 주세요.

2. 리포지토리를 clone 받아주세요
   ```sh
   https://github.com/sudog1/wowyoutoo-backend.git
   ```
3. requirements.txt 를 다운받아 주세요
   ```sh
   pip install -r requirements.txt
   ```
4. 루트 디렉도리에 .env 를 생성한 뒤 아래의 형식으로 담아주세요
   ```sh
   DEBUG=True
    SECRET_KEY="YOUR_SECRET_KEY"
    KAKAO_REST_API_KEY="YOUR_KAKAO_API_KEY"
    SOCIAL_AUTH_GITHUB_CLIENT_ID="YOUR_GITHUB_CLIENT_ID"
    SOCIAL_AUTH_GITHUB_SECRET="YOUR_GITHUB_SECRET_KEY"
    OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
    IMP_KEY="YOUR_PORTONE_KEY"
    IMP_SECRET="YOUR_PORTONE_SECRET_KEY"
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- CONTRIBUTING -->
## Contributing

저희 프로젝트에 개선할 점이 보이신다면 아래의 과정을 따라주세요!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- CONTACT -->
## Contact

스파게티코드클럽 - [https://www.notion.so/b025be898ca042ef9a41a8b2b5ee2660](https://www.notion.so/b025be898ca042ef9a41a8b2b5ee2660) - notion

Project Link: [https://github.com/sudog1/wowyoutoo-backend.git](https://github.com/sudog1/wowyoutoo-backend.git)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [Celery를 활용한 비동기 분산 작업](https://www.notion.so/Celery-aa7b0607d381467aa5b3034161ac718e)
* [OAuth 구현](https://www.notion.so/OAuth-097483a7f83c42b78cbf34d9a3c21859)
* [Channels를 활용한 웹 소켓 구현](https://www.notion.so/Channels-a2a80848fe94494180c884f404fe8899)
* [PortOne api를 활용한 결제 시스템](https://www.notion.so/PortOne-api-af97108e76184d63abb757a2e93db3a9)
* [Docker를 사용한 배포](https://www.notion.so/Docker-6d1f8d20a0484bdfac1a145de873aad4)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/othneildrew/Best-README-Template.svg?style=for-the-badge
[contributors-url]: https://github.com/othneildrew/Best-README-Template/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/othneildrew/Best-README-Template.svg?style=for-the-badge
[forks-url]: https://github.com/othneildrew/Best-README-Template/network/members
[stars-shield]: https://img.shields.io/github/stars/othneildrew/Best-README-Template.svg?style=for-the-badge
[stars-url]: https://github.com/othneildrew/Best-README-Template/stargazers
[issues-shield]: https://img.shields.io/github/issues/othneildrew/Best-README-Template.svg?style=for-the-badge
[issues-url]: https://github.com/othneildrew/Best-README-Template/issues
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/othneildrew/Best-README-Template/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/othneildrew
[product-screenshot]: images/screenshot.png
[Python.com]: https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white
[Python-url]: https://www.python.org/
[VanillaJS.com]:  https://img.shields.io/badge/Javascript-grey?style=for-the-badge&logo=javascript
[VanillaJS-url]: http://vanilla-js.com/
[Django.com]: https://img.shields.io/badge/django-092E20?style=for-the-badge&logo=django&logoColor=white
[Django-url]: https://www.djangoproject.com/
[CSS.com]: https://img.shields.io/badge/css3-1572B6?style=for-the-badge&logo=css3&logoColor=white
[CSS-url]: https://css3.com/
[Python.com]: https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white
[Python-url]: https://www.python.org/
[Celery.com]: https://img.shields.io/badge/celery-37814A?style=for-the-badge&logo=celery&logoColor=white
[Celery-url]: https://docs.celeryq.dev/en/stable/
[Redis.com]: https://img.shields.io/badge/redis-DC382D?style=for-the-badge&logo=redis&logoColor=white
[Redis-url]: https://redis.io/
[OpenAI.com]: https://img.shields.io/badge/openai-412991?style=for-the-badge&logo=openai&logoColor=white
[OpenAI-url]: https://openai.com/
[Docker.com]: https://img.shields.io/badge/docker-2496ED?style=for-the-badge&logo=docker&logoColor=white
[Docker-url]: https://www.docker.com/
[AmazonAWS.com]: https://img.shields.io/badge/amazonaws-232F3E?style=for-the-badge&logo=amazonaws&logoColor=white
[AmazonAWS-url]: https://aws.amazon.com/ko/free/?gclid=CjwKCAiA1MCrBhAoEiwAC2d64dTG9Nx275pggSOsEhCFlbDYVSbrm3r0n7RueNUdbOmoQNL1MVzuGRoCO4gQAvD_BwE&trk=fa2d6ba3-df80-4d24-a453-bf30ad163af9&sc_channel=ps&ef_id=CjwKCAiA1MCrBhAoEiwAC2d64dTG9Nx275pggSOsEhCFlbDYVSbrm3r0n7RueNUdbOmoQNL1MVzuGRoCO4gQAvD_BwE:G:s&s_kwcid=AL!4422!3!563761819837!e!!g!!amazon%20aws!15286221779!129400439506&all-free-tier.sort-by=item.additionalFields.SortRank&all-free-tier.sort-order=asc&awsf.Free%20Tier%20Types=*all&awsf.Free%20Tier%20Categories=*all
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com 
