from rest_framework import permissions
from django.db.models.query import QuerySet
class ReadOnlyPermission(permissions.BasePermission):
    #has_permission 함수를 오버라이딩,view매개변수에는 views.py의 특정 뷰가 들어갈수있다함니다
    def has_permission(self, request, view):
        # GET 요청 또는 사용자가 어드민일 때 권한 부여
        if request.method in permissions.SAFE_METHODS:
            return True
    
        # 사용자가 인증되어 있고 어드민인지 확인
        return request.user.is_authenticated and getattr(request.user, 'is_admin', False)
       


        
        