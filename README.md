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
  <a href="https://github.com/othneildrew/Best-README-Template">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Wow!YouToo?</h3>

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
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][product-screenshot]](https://wowyoutoo.me/main.html)

스픽, 산타토익 등 AI 를 이용한 언어학습이 상업적인 아이디어로 주목받고 있는 가운데, 저희는 이러한 사이트 중 '가볍게' 영어공부를 할 수 있는 사이트는 찾아볼 수 없다고 생각했습니다. 바쁜 현대 사회에서 길게 시간을 내어 영어공부를 하기란 큰 결심이 필요한 일이죠. 바로 그러한 이유로, 와!너두? 가 출시되었습니다.

## 와!너두? 는 이런 분들을 위해 만들어졌습니다.

* 틈틈히 영어공부를 하고 싶었지만 진짜 사람과 대화하기는 부담스러웠던 분들
* 긴 시간을 영어 공부에 할애하기 어려운 분들
* 기초적인 어휘부터 어려운 독해까지 한 번에 경험해보고 싶은 분들



<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

* [![VanillaJS][VanillaJS.com]][VanillaJS-url]
* [![Django][Django.com]][Django-url]
* [![CSS][CSS.com]][CSS-url]
* [![Python][Python.com]][Python-url]
* [![Celery][Celery.com]][Celery-url]
* [![Redis][Redis.com]][Redis-url]
* [![OpenAI][OpenAI.com]][OpenAI-url]
* [![PortOne][PortOne.com]][PortOne-url]
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

API 키와 url 을 .env 파일에 담아주세요

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

Use this space to list resources you find helpful and would like to give credit to. I've included a few of my favorites to kick things off!

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
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com 
