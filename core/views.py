from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from django.db import transaction

from .models import CustomUser, LibraryItem, LendingRecord, ReturnTransaction, Penalty, Payment
from .serializers import (
    CustomUserSerializer, CustomUserCreateSerializer,
    LibraryItemSerializer,
    LendingRecordSerializer,
    ReturnTransactionSerializer,
    PenaltySerializer,
    PaymentSerializer
)
from .permissions import IsAdminUser, IsRegularUser


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['create']:
            return CustomUserCreateSerializer
        return CustomUserSerializer

    def get_permissions(self):
        if self.action in ['list', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticated()]


class LibraryItemViewSet(viewsets.ModelViewSet):
    queryset = LibraryItem.objects.all()
    serializer_class = LibraryItemSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    @action(detail=False, methods=['get'])
    def available(self, request):
        """List all available items."""
        items = LibraryItem.objects.filter(available_stock__gt=0)
        serializer = self.get_serializer(items, many=True)
        return Response(serializer.data)


class LendingRecordViewSet(viewsets.ModelViewSet):
    queryset = LendingRecord.objects.all()
    serializer_class = LendingRecordSerializer
    permission_classes = [IsAuthenticated, IsRegularUser]

    def perform_create(self, serializer):
        user = self.request.user
        item_id = serializer.validated_data['item'].id

        # Start a database transaction to handle concurrency
        with transaction.atomic():
            # Lock the item row to prevent simultaneous modifications
            item = LibraryItem.objects.select_for_update().get(id=item_id)

            # Check if the item is available
            if not item.check_availability():
                raise ValidationError(f"The item '{item.name}' is currently not available.")

            # Check if the user has reached their borrowing limit
            if LendingRecord.objects.filter(borrower=user, is_returned=False).count() >= 5:
                raise ValidationError("You have reached your borrowing limit.")

            item.lend_item()  # Reduce available stock
            serializer.save(borrower=user)

    def get_queryset(self):
        user = self.request.user
        if user.account_type == 'regular':
            return self.queryset.filter(borrower=user)
        return self.queryset


class ReturnTransactionViewSet(viewsets.ModelViewSet):
    queryset = ReturnTransaction.objects.all()
    serializer_class = ReturnTransactionSerializer
    permission_classes = [IsAuthenticated, IsRegularUser]

    def perform_create(self, serializer):
        lending_record = serializer.validated_data['lending_record']

        # Check if the item has already been returned
        if lending_record.is_returned:
            raise ValidationError({"error": "This item has already been returned."})

        # Proceed to save the return transaction if not already returned
        serializer.save()


class PenaltyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Penalty.objects.all()
    serializer_class = PenaltySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Ensure regular users only view their penalties."""
        user = self.request.user
        if user.account_type == 'regular':
            return self.queryset.filter(lending_record__borrower=user)
        return self.queryset


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated, IsRegularUser]

    def perform_create(self, serializer):
        lending_record = serializer.validated_data['lending_record']
        penalty = serializer.validated_data.get('penalty')

        # Ensure the item has been returned before payment
        if not lending_record.is_returned:
            raise ValidationError({"error": "The item must be returned before processing payment."})

        # Handle penalty payment logic
        if penalty and not penalty.is_paid:
            penalty.is_paid = True
            penalty.save()

        serializer.save()
