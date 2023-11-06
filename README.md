# 설치한 패키지
- django 
- djangorestframework 
- djangorestframework-jwt 
- django-cors-headers

# 커밋 컨벤션

## `<type>(<scope>): <message>`

### type(필수)
- feat: 새로운 기능 추가
- fix: 버그 수정 또는 typo
- refactor: 리팩토링
- design: CSS 등 사용자 UI 디자인 변경
- comment: 필요한 주석 추가 및 변경
- style: 코드 포맷팅, 세미콜론 누락, 코드 변경이 없는 경우
- test: 테스트(테스트 코드 추가, 수정, 삭제, 비즈니스 로직에 변경이 없는 경우)
- chore: 위에 걸리지 않는 기타 변경사항(빌드 스크립트 수정, assets image, 패키지 매니저 등)
- init: 프로젝트 초기 생성
- rename: 파일 혹은 폴더명 수정하거나 옮기는 경우
- remove: 파일을 삭제하는 작업만 수행하는 경우

### scope(옵션)
커밋이 영향을 주는 코드의 특정 부분이나 구성 요소

- auth: 인증 관련

### message(필수)
짧고 간결하게 구현한 기능을 설명해 주세요.
예시: "로그인 인증 구현"
잘못된 예시: "유저의 로그인 인증을 구현하였습니다"

### 커밋 메시지 예시
feat(auth): 구글 로그인 추가
fix(validation): 유저 로그인 데이터 검증
chore(docs): README에 그라운드룰 추가
test(user-profile): 유저 프로필 조회 테스트