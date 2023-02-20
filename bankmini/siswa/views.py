from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from siswa.models import *
from siswa.forms import *
from django.contrib.auth import authenticate, login, logout

# Create your views here.
class IndexView(View):
    def get(self, request):
        if request.user.is_authenticated:
            current_user = request.user
            rekening=Rekening.objects.all().filter(user_id=current_user)    
            # profile=ProfileUser.objects.filter(file_type='image') 
            username = request.user.username
            content = {
                'username': username,
                'rekening': rekening,  
            }
            return render(request, 'index.html', content)
        else:
            return redirect('login/')
    
class DashboardView(View):
    def get(self, request):
        rekening=Rekening.objects.get(user_id=request.user)
        history_id=History.objects.latest('id')
        history=History.objects.all().filter(rekening=rekening).order_by('-waktu')

        content = {
            'history': history,
            'history_id': history_id,
        }
        return render(request, 'dashboard.html', content)  

class ProfileView(View):
    def get(self, request):
        username = request.user.username
        email = request.user.email
        profile=ProfileUser.objects.all().filter(user_id=request.user)
        content = {
                'username': username,
                'email': email,
                'profile': profile,
            }
        return render(request, 'profile.html', content)

class PrivacyView(View):
    def get(self, request):
        return render(request, 'privacy.html')

class TransferView(View):
    def post(self, request):
        transaction_type= 'transfer'
        user_from= Rekening.objects.get(user_id__id= request.user.id)
        user_to= Rekening.objects.get(user_id= request.POST['user_to'])
        amount= float(request.POST['amount'])

        saldoPengirimBaru = user_from.saldo - amount
        saldoPenerimaBaru = user_to.saldo + amount

        Transaction.objects.create(transaction_type=transaction_type, amount=amount, user_from=user_from, user_to=user_to)

        Rekening.objects.filter(user_id__id= request.user.id).update(
            saldo= saldoPengirimBaru
        )
        Rekening.objects.filter(user_id__id= request.POST['user_to']).update(
            saldo= saldoPenerimaBaru
        )

        return redirect('/')

    def get(self, request):
        rekening=Rekening.objects.all()
        content = {
            'rekening': rekening
        }
        return render(request, 'transfer.html', content)

class LoginView(View):
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            if user.is_superuser:
                return redirect('/admin')
            else:
                return redirect('/../')
        else:
            return redirect('/')

    def get(self, request):
        return render(request, 'login.html')

def LogoutView(request):
    logout(request)
    return redirect('../login/')

class RegisterView(View):
    def post(self, request):
        if request.method=="POST":
            username=request.POST['username']
            first_name=request.POST['first_name']
            last_name=request.POST['last_name']
            email=request.POST['email']
            password=request.POST['password']
            obj=User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password)
        obj.save()
        return redirect('/')
    def get(self, request):
        return render(request, 'register.html')