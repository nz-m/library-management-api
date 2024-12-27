from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views  # Import the views module

router = DefaultRouter()
router.register('users', views.CustomUserViewSet, basename='user')
router.register('library-items', views.LibraryItemViewSet, basename='libraryitem')
router.register('lending-records', views.LendingRecordViewSet, basename='lendingrecord')
router.register('return-transactions', views.ReturnTransactionViewSet, basename='returntransaction')
router.register('penalties', views.PenaltyViewSet, basename='penalty')
router.register('payments', views.PaymentViewSet, basename='payment')

urlpatterns = [
    path('', include(router.urls)),
]
