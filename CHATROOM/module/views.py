from django.http import JsonResponse
from django.shortcuts import render, redirect, reverse , get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout,login
from .forms import LoginForm, RegisterForm, EditProfileModelForm, ChangePasswordForm
from .models import User , Message , Report
from rest_framework import status
from rest_framework.decorators import api_view , permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from .serializers import UserSerializer , MessageSerializer , ReportSerializer
# Create your views here.

def aboutus(request):
    return render(request, 'module/About us.html')

def invalid_path(request,invalid_path):
    return render(request, 'module/Not found.html',status=404)

def logout_view(request):
    logout(request)
    return redirect(reverse('login'))

def login_view(request):
    if request.user.is_authenticated:
        return redirect(reverse('chatroom'))
    if request.method == 'GET':
        login_form = LoginForm()
        context = {'login_form': login_form}
        return render(request, 'module/Login.html', context)

    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_email = login_form.cleaned_data.get('email')
            user_pass = login_form.cleaned_data.get('password')
            user = User.objects.filter(email__iexact=user_email).first()
            if user is not None:
                is_password_correct = user.check_password(user_pass)
                if is_password_correct:
                    login(request, user)
                    return JsonResponse({
                        'status': 'success',
                        'text': 'login success.',
                        'icon': 'success'
                    })
                else:
                    return JsonResponse({
                        'status': 'invalid input',
                        'text': 'the information is not correct.',
                        'icon': 'error'
                    })
            else:
                return JsonResponse({
                    'status': 'invalid input',
                    'text': 'the information is not correct.',
                    'icon': 'error'
                })

        context = {'login_form': login_form}
        return render(request, 'module/Login.html', context)

def signup(request):
    if request.method == 'GET':
        register_form = RegisterForm()
        return render(request, "module/Sign up.html", {'register_form': register_form})

    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = register_form.cleaned_data.get('name')
            user_family = register_form.cleaned_data.get('family')
            user_email = register_form.cleaned_data.get('email')
            user_password = register_form.cleaned_data.get('password')
            user_confirm_password = register_form.cleaned_data.get('confirm_password')
            user_exists = User.objects.filter(email__iexact=user_email).exists()
            if user_exists:
                return JsonResponse({
                    'status': 'invalid input',
                    'text': 'your email is already in use.',
                    'icon': 'error'
                })
            elif user_password != user_confirm_password:
                return JsonResponse({
                    'status': 'invalid input',
                    'text': 'The password is not the same as its repetition!',
                    'icon': 'error'
                })
            else:
                new_user = User(
                    username=user_email,
                    first_name=user_name,
                    last_name=user_family,
                    email=user_email,
                    is_active=True
                )
                new_user.set_password(user_password)
                new_user.save()
                login(request, new_user)
                return JsonResponse({
                    'status': 'success',
                    'text': 'signup success.',
                    'icon': 'success'
                })
        context = {'register_form': register_form}
        return render(request, "module/Sign up.html", context)

@login_required
def account(request):
    return render(request, "module/Account.html")

@login_required
def changeinformation(request):
    if request.method == 'GET':
        userdata = User.objects.filter(id=request.user.id).first()
        edit_form = EditProfileModelForm(instance=userdata)
        context = {
            'form': edit_form,
            'user': userdata
        }
        return render(request, 'module/Change inforamtion.html', context)

    if request.method == 'POST':
        userdata = User.objects.filter(id=request.user.id).first()
        edit_form = EditProfileModelForm(request.POST, request.FILES,instance=userdata)
        if edit_form.is_valid():
            edit_form.save()
            return JsonResponse({
                'status': 'success',
                'text': 'change success.',
                'icon': 'success'
            })
        else:
            error_messages = []
            for field, errors in edit_form.errors.items():
                for error in errors:
                    error_messages.append(error)
            error_text = "\n".join(error_messages)

            return JsonResponse({
                'status': 'invalid input',
                'text': error_text,
                'icon': 'error'
            })

@login_required
def changepassword(request):
    if request.method == 'GET':
        form = ChangePasswordForm()
        context = {
            'form': form
        }
        return render(request, 'module/Change password.html', context)
    elif request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            user = User.objects.filter(id=request.user.id).first()
            if user.check_password(form.cleaned_data.get('current_password')):
                user.set_password(form.cleaned_data.get('password'))
                user.save()
                logout(request)
                return JsonResponse({
                    'status': 'success',
                    'text': 'change success.',
                    'icon': 'success'
                })
            else:
                return JsonResponse({
                    'status': 'invalid input',
                    'text': 'the password entered is incorrect!',
                    'icon': 'error',
                })
        else:
            error_messages = []
            for field, errors in form.errors.items():
                for error in errors:
                    error_messages.append(error)
            error_text = "\n".join(error_messages)

            return JsonResponse({
                'status': 'invalid input',
                'text': error_text,
                'icon': 'error'
            })

@login_required
def chatroom(request):
    message = Message.objects.all()
    context={
        'message': message
    }
    return render(request,'module/Chat Room.html',context)


@login_required
def sendmessage(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        parent_id = request.POST.get('parent_id')
        file = request.FILES.get('file')

        if not message and not file:
            return JsonResponse({
                'status': 'invalid input',
                'text': 'At least one message or file must be sent.',
                'icon': 'error',
            })

        parent_message = None
        if parent_id:
            try:
                parent_message = Message.objects.get(id=parent_id)
            except Message.DoesNotExist:
                parent_message = None

        new_message = Message(user=request.user, parent_id=parent_message)

        if message:
            new_message.content = message

        if file:
            file_type = file.content_type
            if file_type.startswith('image/'):
                new_message.image = file
            elif file_type.startswith('audio/'):
                new_message.audio = file
            else:
                return JsonResponse({
                    'status': 'invalid input',
                    'text': 'Only image or audio formats are supported.',
                    'icon': 'error',
                })

        new_message.save()
        context = {
            'mes': new_message
        }
        return render(request, 'module/Send message.html', context)

    return JsonResponse({
        'status': 'invalid method',
        'text': 'Only POST requests are allowed.',
        'icon': 'error',
    })
        
@login_required
def report(request):
    if request.method == "POST":
        message_id = request.POST.get("message_id")
        user = request.user
        message = get_object_or_404(Message, pk=message_id)
        if Report.objects.filter(reporter=user, message=message).exists():
            return JsonResponse({"error": "You have already reported this message."}, status=400)
        Report.objects.create(reporter=user, message=message)
        return JsonResponse({"message": "Reported successfully"})
    return JsonResponse({"error": "Invalid request"}, status=400)

@login_required
def delete(request, pk):
    if request.method == 'POST':
        message = get_object_or_404(Message, pk=pk, user=request.user)
        message.delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error', 'text': 'Invalid request'})

MAX_AVATAR_SIZE_MB = 2
ALLOWED_IMAGE_TYPES = ['image/jpeg', 'image/png', 'image/webp']
@extend_schema(
    request={
        'multipart/form-data': {
            'type': 'object',
            'properties': {
                'username': {'type': 'string'},
                'first_name': {'type': 'string'},
                'last_name': {'type': 'string'},
                'email': {'type': 'string', 'format': 'email'},
                'password': {'type': 'string', 'format': 'password'},
                'confirm_password': {'type': 'string', 'format': 'password'},
                'avatar': {'type': 'string', 'format': 'binary'},
            },
            'required': ['username', 'first_name' , 'last_name' , 'email', 'password','confirm_password']
        }
    }
)
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def user_list_create(request):
    if request.method == 'GET':
        if not request.user.is_staff:
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        password = request.data.get('password')
        confirm_password = request.data.get('confirm_password')
        if password != confirm_password:
            return Response({'detail': 'Passwords do not match.'}, status=status.HTTP_400_BAD_REQUEST)
        data = request.data.copy()
        data.pop('confirm_password', None)
        if User.objects.filter(username=data.get('username')).exists():
            return Response({'username': ['Username already exists.']}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(email=data.get('email')).exists():
            return Response({'email': ['Email already exists.']}, status=status.HTTP_400_BAD_REQUEST)
        avatar = request.FILES.get('avatar')
        if avatar:
            if avatar.content_type not in ALLOWED_IMAGE_TYPES:
                return Response({'avatar': ['Invalid image format.']}, status=status.HTTP_400_BAD_REQUEST)
            if avatar.size > MAX_AVATAR_SIZE_MB * 1024 * 1024:
                return Response({'avatar': ['Image size too large.']}, status=status.HTTP_400_BAD_REQUEST)
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(password)
            user.save()
            response_data = UserSerializer(user).data
            response_data.pop('password', None)
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    request={
        'multipart/form-data': {
            'type': 'object',
            'properties': {
                'username': {'type': 'string'},
                'first_name': {'type': 'string'},
                'last_name': {'type': 'string'},
                'email': {'type': 'string', 'format': 'email'},
                'password': {'type': 'string', 'format': 'password'},
                'confirm_password': {'type': 'string', 'format': 'password'},
                'avatar': {'type': 'string', 'format': 'binary'},
            },
            'required': ['username', 'first_name' , 'last_name' , 'email', 'password','confirm_password']
        }
    }
)
@api_view(['GET', 'PUT'])
def user_detail_update(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    if request.user != user and not request.user.is_staff:
        return Response({'error': 'You do not have permission to access this user.'}, status=status.HTTP_403_FORBIDDEN)
    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)
    elif request.method == 'PUT':
        data = request.data.copy()
        avatar = request.FILES.get('avatar')
        if avatar:
            if avatar.content_type not in ALLOWED_IMAGE_TYPES:
                return Response({'avatar': ['Invalid image format.']}, status=status.HTTP_400_BAD_REQUEST)
            if avatar.size > MAX_AVATAR_SIZE_MB * 1024 * 1024:
                return Response({'avatar': ['Image size too large.']}, status=status.HTTP_400_BAD_REQUEST)
            data['avatar'] = avatar
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        if password or confirm_password:
            if password != confirm_password:
                return Response(
                    {'confirm_password': ['Password and confirm password do not match.']},
                    status=status.HTTP_400_BAD_REQUEST
                )
        serializer = UserSerializer(user, data=data, partial=True)
        if serializer.is_valid():
            user = serializer.save()
            if password:
                user.set_password(password)
                user.save()
            response_data = UserSerializer(user).data
            response_data.pop('password', None)
            return Response(response_data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    request={
        'multipart/form-data': {
            'type': 'object',
            'properties': {
                'message_id': {'type': 'integer'}
            },
            'required': ['message_id']
        }
    }
)
@api_view(['POST'])
def report_message_api(request):
    message_id = request.data.get('message_id')
    if not message_id:
        return Response({'message_id': ['This field is required.']}, status=status.HTTP_400_BAD_REQUEST)
    message = get_object_or_404(Message, id=message_id)
    if Report.objects.filter(reporter=request.user, message=message).exists():
        return Response({'detail': 'You have already reported this message.'}, status=status.HTTP_400_BAD_REQUEST)
    serializer = ReportSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(reporter=request.user, message=message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    request={
        'multipart/form-data': {
            'type': 'object',
            'properties': {
                'parent_id': {'type': 'integer'},
                'content': {'type': 'string'},
                'image': {'type': 'string', 'format': 'binary'},
                'audio': {'type': 'string', 'format': 'binary'}
            }
        }
    }
)  
@api_view(['GET', 'POST'])
def message_api(request):
    if request.method == 'GET':
        if not request.user.is_staff:
            return Response({'detail': 'Permission denied.'}, status=403)
        messages = Message.objects.all().order_by('-timestamp')
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        content = request.data.get('content')
        image = request.FILES.get('image')
        audio = request.FILES.get('audio')
        if not content and not image and not audio:
            return Response(
                {"detail": "You must provide content, or an image, or an audio."},
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'parent_id': request.data.get('parent_id'),
            'content': content,
            'image': image,
            'audio': audio
        }
        if str(data.get('parent_id')) == '0':
            data.pop('parent_id')
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    request=MessageSerializer
)    
@api_view(['GET', 'DELETE'])
def message_detail(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    if not (request.user.is_staff or message.user == request.user):
        return Response({'detail': 'Permission denied.'}, status=403)
    if request.method == 'GET':
        serializer = MessageSerializer(message)
        return Response(serializer.data)
    elif request.method == 'DELETE':
        message.delete()
        return Response({'detail': 'Message deleted successfully.'}, status=204)