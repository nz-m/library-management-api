from rest_framework import serializers
from .models import CustomUser, LibraryItem, LendingRecord, ReturnTransaction, Penalty, Payment


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'account_type', 'date_created', 'last_updated']
        read_only_fields = ['account_type', 'date_created', 'last_updated']


class CustomUserCreateSerializer(serializers.ModelSerializer):
    account_type = serializers.CharField()

    """For user registration"""
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password', 'account_type']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            account_type=validated_data['account_type']
        )
        return user


class LibraryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = LibraryItem
        fields = ['id', 'name', 'writer', 'identifier', 'total_stock', 'available_stock', 'date_added', 'last_modified']
        read_only_fields = ['available_stock', 'date_added', 'last_modified']

    def validate_total_stock(self, value):
        if value <= 0:
            raise serializers.ValidationError("Total stock must be greater than zero.")
        return value


class LendingRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = LendingRecord
        fields = ['id', 'item', 'date_borrowed', 'due_date', 'is_returned', 'created_on', 'updated_on']
        read_only_fields = ['date_borrowed', 'due_date', 'is_returned', 'created_on', 'updated_on']

    def validate(self, data):
        request = self.context.get('request')
        user = request.user
        item = data['item']

        if LendingRecord.objects.filter(borrower=user, is_returned=False).count() >= 5:
            raise serializers.ValidationError("You have reached your borrowing limit of 5 items.")

        if not item.check_availability():
            raise serializers.ValidationError(f"The item '{item.name}' is currently not available.")

        return data

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        validated_data['borrower'] = user  # Assign the borrower to the validated data

        item = validated_data['item']
        item.lend_item()  # Reduce available stock
        return super().create(validated_data)


class ReturnTransactionSerializer(serializers.ModelSerializer):
    penalty = serializers.SerializerMethodField()

    class Meta:
        model = ReturnTransaction
        fields = ['id', 'lending_record', 'date_returned', 'penalty_paid', 'penalty', 'created_on', 'updated_on']
        read_only_fields = ['date_returned', 'penalty', 'created_on', 'updated_on']

    def get_penalty(self, obj):
        return obj.compute_penalty()

    def create(self, validated_data):
        return_transaction = super().create(validated_data)
        lending_record = return_transaction.lending_record
        lending_record.is_returned = True
        lending_record.item.return_item()  # Increase available stock
        lending_record.save()
        return return_transaction


class PenaltySerializer(serializers.ModelSerializer):
    class Meta:
        model = Penalty
        fields = ['id', 'lending_record', 'amount', 'is_paid', 'created_on', 'updated_on']
        read_only_fields = ['amount', 'created_on', 'updated_on']


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'lending_record', 'penalty', 'payment_date', 'amount_settled', 'created_on', 'updated_on']
        read_only_fields = ['payment_date', 'created_on', 'updated_on']
