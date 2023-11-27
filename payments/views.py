from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Payment, Product
from .serializers import PrepareSerializer, ProductSerializer
import requests
import json
from pathlib import Path
import environ



class ProductListView(ListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.filter(status=Product.Status.ACTIVE)


# 결제 전 검증을 위한 주문번호, 결제 예정 금액 DB 저장
class PrepareView(APIView):
    def post(self, request):
        # Need serializer?
        serializer = PrepareSerializer(data=request.data, context={"email": request.user.email})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# 결제 후 검증
class CompleteView(APIView):
    BASE_DIR = Path(__file__).resolve().parent.parent
    env = environ.Env()
    env.read_env(BASE_DIR / ".env")
    IMP_KEY = env("IMP_KEY")
    IMP_SECRET = env("IMP_SECRET")
    
    # access token 발급 요청
    def get_token_api(self):
        API_HOST = "https://api.iamport.kr"
        path = "/users/getToken"
        url = f"{API_HOST}{path}"
        
        headers = {"Content-Type": "application/json", "charset": "UTF-8", "Accept": "*/*"}
        body = {
            "imp_key": self.IMP_KEY, # REST API Key
            "imp_secret": self.IMP_SECRET # REST API Secret
        }
        try:
            response = requests.post(url, headers=headers, data=json.dumps(body, ensure_ascii=False, indent="\t"))
            json_object = response.json() # json 객체로 변환
            token_val = json_object["response"]["access_token"] # 토큰값 파싱
            print(token_val)
            return token_val
        except Exception as ex:
            return None
    
    
    def post(self, request):
        #PortOne으로부터 imp_uid, merchant_uid 수신
        imp_uid = request.data.get("imp_uid")
        merchant_uid = request.data.get("merchant_uid")
        order = get_object_or_404(Payment, merchant_uid=merchant_uid)
        
        #Get the access token
        access_token = self.get_token_api()
        
        if access_token:
            iamport_url = f"https://api.iamport.kr/payments/{imp_uid}"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}" 
            }
        
            try:
                response = requests.get(iamport_url, headers=headers)
                response_data = response.json()
                
                #결제 검증
                amount_to_be_paid = order.amount
                paid_amount = response_data.get("response", {}).get("amount")
                print("paid_amount: ", paid_amount)
                if paid_amount == amount_to_be_paid:
                    order.status = response_data.get("response", {}).get("status") #Update the status based on the PortOne response
                    order.paid_amount = paid_amount
                    order.save()
                
                return Response({"detail": "결제 완료"}, status=response.status_code)
            except Exception as ex:
                return Response({"error": str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"error": "access token을 발급받는데 실패했습니다."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # response_data:  {'code': 0, 'message': None, 'response': {'amount': 100, 'apply_num': '00000000', 'bank_code': None, 'bank_name': None, 'buyer_addr': '서울특별시 강남구 신사동', 'buyer_email': 'gildong@gmail.com', 'buyer_name': '홍길동', 'buyer_postcode': '01181', 'buyer_tel': '010-4242-4242', 'cancel_amount': 0, 'cancel_history': [], 'cancel_reason': None, 'cancel_receipt_urls': [], 'cancelled_at': 0, 'card_code': '366', 'card_name': '신한(구.LG카드 포함)카드', 'card_number': '4364200782968521', 'card_quota': 0, 'card_type': 1, 'cash_receipt_issued': False, 'channel': 'pc', 'currency': 'KRW', 'custom_data': None, 'customer_uid': None, 'customer_uid_usage': None, 'emb_pg_provider': None, 'escrow': False, 'fail_reason': None, 'failed_at': 0, 'imp_uid': 'imp_850683311385', 'merchant_uid': 'a07ed0aa-af71-45ca-91ab-cfc513edd72f', 'name': '노르웨이 회전 의자', 'paid_at': 1701008726, 'pay_method': 'card', 'pg_id': 'tlgdacomxpay', 'pg_provider': 'uplus', 'pg_tid': 'tlgda20231126232526np3s4', 'receipt_url': 'http://pgweb.dacom.net:7085/pg/wmp/etc/jsp/Receipt_Link.jsp?mertid=tlgdacomxpay&tid=tlgda20231126232526np3s4&authdata=f15901ec30ace794dbd9624097263922', 'started_at': 1701008683, 'status': 'paid', 'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36', 'vbank_code': None, 'vbank_date': 0, 'vbank_holder': None, 'vbank_issued_at': 0, 'vbank_name': None, 'vbank_num': None}}