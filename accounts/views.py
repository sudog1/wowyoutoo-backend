from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404
from accounts.models import User
from rest_framework_simplejwt.views import TokenObtainPairView
from accounts.serializers import LoginSerializer, UserSerializer


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer


class SignupView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # 이메일 확인 토큰 생성
            # token = default_token_generator.make_token(user)
            # uid = urlsafe_base64_encode(force_bytes(user.pk))

            # # 이메일에 확인 링크 포함하여 보내기
            # verification_url = f"http://127.0.0.1:8000/users/verify-email/{uid}/{token}/"
            # # 이메일 전송 코드 작성 및 이메일에 verification_url을 포함하여 보내기

            # # 이메일 전송
            # # subject = '이메일 확인 링크'
            # # message = f'이메일 확인을 완료하려면 다음 링크를 클릭하세요: {verification_url}'
            # # from_email = 'estherwoo01@gmail.com'
            # # recipient_list = [user.email]

            # # send_mail(subject, message, from_email, recipient_list)

            # send_verification_email.delay(
            #     user.id, verification_url, user.email)

            return Response({"message": "회원가입 성공!"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
