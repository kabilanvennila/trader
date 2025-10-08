from rest_framework import serializers
from .models import Trade, Strike, Transfer

class StrikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Strike
        fields = ["id", "strike_price", "option_type", "position", "lots", "expiry_date", "ltp"]

class TradeSerializer(serializers.ModelSerializer):
    strikes = StrikeSerializer(many=True, read_only=True)

    class Meta:
        model = Trade
        fields = [
            "id", "indices_stock", "bias", "setup", "strategy", "days_to_expiry",
            "main_lots", "price_per_unit", "hedge_lots", "price_per_hedge_unit",
            "max_profit", "max_loss", "capital", "notes", "status",
            "created_at", "strikes"
        ]

class TradeCreateSerializer(serializers.ModelSerializer):
    strikes = StrikeSerializer(many=True)

    class Meta:
        model = Trade
        fields = "__all__"

    def create(self, validated_data):
        strikes_data = validated_data.pop("strikes", [])
        trade = Trade.objects.create(**validated_data)
        for s in strikes_data:
            Strike.objects.create(trade=trade, **s)
        return trade

    def update(self, instance, validated_data):
        strikes_data = validated_data.pop("strikes", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if strikes_data is not None:
            instance.strikes.all().delete()
            for s in strikes_data:
                Strike.objects.create(trade=instance, **s)
        
        return instance

class TransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transfer
        fields = ["id", "date", "type", "amount", "notes", "created_at", "updated_at"]
    
    def get_formatted_amount(self, obj):
        sign = "+" if obj.type == "DEPOSIT" else "-"
        return f"{sign}₹{int(obj.amount):,}"
