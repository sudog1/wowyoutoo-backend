import logging
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db import transaction
from .models import Payment, Product, CartItem, OrderItem
from .serializers import PrepareSerializer, ProductSerializer, NestedListSerializer
import requests
import json
from pathlib import Path
import environ


# 상품 리스트 페이지
class ProductListView(ListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.filter(status=Product.Status.ACTIVE)


class CartView(APIView):
    permission_classes = [IsAuthenticated]
    
    # cart에 물건 담기
    def post(self, request, product_id):
        #재고 있는 product 중, 선택된 product를 가져옴
        product_active = Product.objects.filter(status=Product.Status.ACTIVE)
        product = get_object_or_404(product_active, pk=product_id)
        
        # 선택된 수량을 가져옴, default 값은 1개
        quantity = int(request.data.get("quantity", 1))
        
        # 선택된 product와 수량을 cart에 담음
        cart_item, is_created = CartItem.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={"quantity":quantity}
        )
        
        if not is_created:
            cart_item.quantity += quantity
            cart_item.save()
        
        return Response({"message": "Product is added to cart"}, status=status.HTTP_201_CREATED)
    
    # 장바구니 상품 불러오기   
    def get(self, request):
        # 현재 user의 장바구니의 모든 상품들을 가져옴
        items = CartItem.objects.filter(user=request.user)
        
        # 장바구니 페이지에서 보여줄 attributes
        product_names = []
        descriptions = []
        prices = []
        quantities = []
        
        for item in items:
            product_name = item.product.product_name
            description = item.product.description
            price = item.product.price
            quantity = item.quantity
            
            product_names.append(product_name)
            descriptions.append(description)
            prices.append(price)
            quantities.append(quantity)
        
        # 장바구니에 보여줄 상품 정보 보기 좋게 list 형식으로 자리 바꿈   
        transposed_lists = list(zip(product_names, descriptions, prices, quantities))
        
        # Serialize the transposed lists
        serialized_data = [NestedListSerializer(data={"product_name": row[0], "description": row[1], "price": row[2], "quantity": row[3]}) for row in transposed_lists]
        
        # serializer 검증
        for serializer in serialized_data:
            serializer.is_valid(raise_exception=True)
        
        # Get the serialized data
        serialized_data = [serializer.validated_data for serializer in serialized_data]

        return Response(serialized_data, status=status.HTTP_201_CREATED)
    
    # 장바구니 업데이트
    def put(self, request):
        try:
            updated_products = request.data.get("updatedProducts", [])

            for updated_product in updated_products:
                product_name = updated_product.get("product_name")
                quantity = int(updated_product.get("quantity", 1))
                
                product = Product.objects.get(product_name=product_name)
                cart_item = CartItem.objects.get(user=request.user, product=product)

                cart_item.quantity = quantity
                cart_item.save()
                
            # 현재 user의 장바구니의 모든 상품들을 가져옴
            items = CartItem.objects.filter(user=request.user)
            
            # 장바구니 페이지에서 보여줄 attributes
            product_names = []
            descriptions = []
            prices = []
            quantities = []
            
            for item in items:
                product_name = item.product.product_name
                description = item.product.description
                price = item.product.price
                quantity = item.quantity
                
                product_names.append(product_name)
                descriptions.append(description)
                prices.append(price)
                quantities.append(quantity)

            # 장바구니에 보여줄 상품 정보 보기 좋게 list 형식으로 자리 바꿈   
            transposed_lists = list(zip(product_names, descriptions, prices, quantities))

            # Serialize the transposed lists
            serialized_data = [NestedListSerializer(data={"product_name": row[0], "description": row[1], "price": row[2], "quantity": row[3]}) for row in transposed_lists]

            # serializer 검증
            for serializer in serialized_data:
                serializer.is_valid(raise_exception=True)
            
            # Get the serialized data
            serialized_data = [serializer.validated_data for serializer in serialized_data]

            return Response(serialized_data, status=status.HTTP_200_OK)
                        
        except CartItem.DoesNotExist:
            return Response({"error": "CartItem not found"}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# 결제 전 검증을 위한 주문번호, 결제 예정 금액 DB 저장
class PrepareView(APIView):
    def post(self, request):
        # 현재 user의 장바구니 상품들 모두 가져옴
        items = CartItem.objects.filter(user=request.user)
        
        # 결제해야 할 금액
        total_price_tobe_paid = 0 
        
        for item in items:
            price = item.product.price
            quantity = item.quantity
            
            total_price_tobe_paid += price * quantity
            
        merchant_uid = request.data.get("merchant_uid")
        product_name = request.data.get("product_name")
        user = request.user
        
        request.data["amount"] = total_price_tobe_paid
        
        # Payment object 생성
        payment = Payment.objects.create(
            user=user,
            merchant_uid = merchant_uid,
            amount = total_price_tobe_paid,
            product_name = product_name
        )
        
        # 현재 user의 cart에 들어있는 상품들에게 payment_id 값을 assign
        for item in items:
            item.payment_id = payment
            item.save()
        
        serializer = PrepareSerializer(instance=payment)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


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
            # print(token_val)
            return token_val
        except Exception as ex:
            return None
    
    
    def post(self, request):
        #PortOne으로부터 imp_uid, merchant_uid 수신
        imp_uid = request.data.get("imp_uid")
        merchant_uid = request.data.get("merchant_uid")
        payment = get_object_or_404(Payment, merchant_uid=merchant_uid)
        
        # Get the access token
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
                amount_to_be_paid = payment.amount
                paid_amount = response_data.get("response", {}).get("amount")

                if paid_amount == amount_to_be_paid:
                    payment.status = response_data.get("response", {}).get("status") #Update the status based on the PortOne response
                    payment.paid_amount = paid_amount
                    payment.save()
                print("payment.user: ", payment.user)

                # 장바구니 속 상품들의 payment_id의 상태 값이 'paid'일 경우,
                # 장바구니 비워주고, Order 테이블에 상품 내역 저장
                if payment.status == "paid":
                    cart_items = CartItem.objects.filter(user=payment.user)

                    # To ensure consistency
                    with transaction.atomic():
                        order_items = []
                        for cart_item in cart_items:    
                            order_item = OrderItem.objects.create(
                                user=payment.user,
                                product=cart_item.product,
                                quantity=cart_item.quantity,
                            )
                            order_items.append(order_item)    
                            
                        cart_items.delete()
                        
                
                return Response({"detail": "결제 완료"}, status=response.status_code)
            
            except Exception as ex:
                logging.error(f"Error: {ex}")
                return Response({"error": str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        else:
            return Response({"error": "access token을 발급받는데 실패했습니다."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
