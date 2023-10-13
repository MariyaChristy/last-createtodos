from rest_framework import serializers
from todoapp.models import Todos

class TofoSerializer(serializers.ModelSerializer):
    user=serializers.CharField(required=True)
    class Meta:
        model=Todos
        fields="__all__"

    def create(self, validated_data):
        user=self.context.get("user")
        return Todos.objects.create(**validated_data,user=user)