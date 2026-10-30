from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'bookings', views.BookingViewSet, basename='booking')

urlpatterns = [
    path('', views.index, name='home'),
    path('api/menu/', views.MenuItemsView.as_view(), name='menu-items'),
    path('api/menu/<int:pk>/', views.SingleMenuItemView.as_view(), name='menu-item'),
    path('api/', include(router.urls)),
]
