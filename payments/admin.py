from django.contrib import admin
from .models import Payment, Product, CartItem

# Register your models here.
admin.site.register(Payment)
admin.site.register(CartItem)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["pk", "product_name", "description", "price", "status"]
    list_display_links = ["product_name"]
    search_fields = ["name"]
    list_filter = ["status", "created_at", "updated_at"]
    date_hierarchy = "updated_at"
    actions = ["make_active"]
    
    @admin.display(description=f"지정된 상품을 {Product.Status.ACTIVE.label} 상태로 변경")
    def make_active(self, request, queryset):
        count = queryset.update(status=Product.Status.ACTIVE)
        self.message_user(
            request, f"{count}개의 상품을 {Product.Status.ACTIVE.label} 상태로 변경 완료"
        )