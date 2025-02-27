from django.http import JsonResponse
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout,login
from .forms import LoginForm, RegisterForm, EditProfileModelForm, ChangePasswordForm
from .models import User , Message
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
    message = request.GET.get('article_comment')
    if message:
        new_comment = Message(content=message, user=request.user)
        new_comment.save()
        context = {
            'mes': new_comment
        }
        return render(request, 'module/Send message.html', context)
    else:
        return JsonResponse({
            'status': 'invalid input',
            'text': 'input should not be empty when submitting.',
            'icon': 'error',
        })
