from rest_framework import serializers
from .models import User, Message, Report


class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(required=False)
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password' , 'avatar']
        extra_kwargs = {
                'password': {'write_only': True}
            }
        

class MessageSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    parent_id = serializers.PrimaryKeyRelatedField(queryset=Message.objects.all(), required=False, allow_null=True)
    class Meta:
        model = Message
        fields = ['id','user','parent_id','content','image','audio','timestamp']
        read_only_fields = ['timestamp']

class ReportSerializer(serializers.ModelSerializer):
    reporter = UserSerializer(read_only=True)
    message = MessageSerializer(read_only=True)
    message_id = serializers.PrimaryKeyRelatedField(queryset=Message.objects.all(),source='message',write_only=True)
    class Meta:
        model = Report
        fields = ['id', 'reporter', 'message', 'message_id', 'timestamp']
        read_only_fields = ['timestamp']