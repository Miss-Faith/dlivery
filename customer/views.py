import json
from django.contrib.auth import authenticate, login, get_user_model
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from .tokens import account_activation_token
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.db.models import Q
from django.core.mail import send_mail
from django.contrib import messages
from .models import *
from .forms import *

# Create your views here.
def Index(request, *args, **kwargs):
    User = get_user_model()
    if request.method == 'POST':
        Signupform = SignupForm(request.POST,request.FILES)
        form = LoginForm(request.POST)
        if request.POST.get('submit') == 'Login':
            username = request.POST.get('username')
            password1 = request.POST.get('password1')

            user = authenticate(request, username=username, password1=password1)

            if user is not None:
                login(request,user)
                return redirect('menu')
            else:
                messages.info(request, 'Wrong Username or password')

            return render(request, 'customer/index.html', {'form':form})

        elif Signupform.is_valid():
            username = Signupform.cleaned_data.get('username')
            email = Signupform.cleaned_data.get('email')
            password = Signupform.cleaned_data.get('password')

            if User.objects.filter(email__iexact=email).count() == 1:
                user = Signupform.save(commit=False)
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                mail_subject = 'Activate your account.'
                message = render_to_string('email_confirm.html', {
                            'user': user,
                            'domain': current_site.domain,
                            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                            'token': account_activation_token.make_token(user),
                        })
                to_email = Signupform.cleaned_data.get('email')
                send_mail(mail_subject, message, 'youremail', [to_email])
                return HttpResponse('Please confirm your email address to complete the registration')
    
    else:
        Signupform = SignupForm()
        form = LoginForm

    return render(request, 'customer/index.html', {'Signupform': Signupform, 'form':form})

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')

def About(request, *args, **kwargs):
    return render(request,'customer/about.html')


class Order(View):
    def get(self, request, *args, **kwargs):
        # get every item from each category
        food = MenuItem.objects.filter(category__name__contains='Food')
        drinks = MenuItem.objects.filter(category__name__contains='Drink')
        groceries = MenuItem.objects.filter(category__name__contains='Grocer')
       
        # pass into context
        context = {
            'food': food,
            'drinks': drinks,
            'groceries': groceries,
        }

        # render the template
        return render(request, 'customer/order.html', context)

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        number = request.POST.get('number')
        address = request.POST.get('address')
        houseno = request.POST.get('houseno')
        

        order_items = {
            'items': []
        }

        items = request.POST.getlist('items[]')

        for item in items:
            menu_item = MenuItem.objects.get(pk__contains=int(item))
            item_data = {
                'id': menu_item.pk,
                'name': menu_item.name,
                'price': menu_item.price
            }

            order_items['items'].append(item_data)

            price = 70
            item_ids = []

        for item in order_items['items']:
            price += item['price']
            item_ids.append(item['id'])

        order = OrderModel.objects.create(
            price=price,
            name=name,
            address=address,
            number=number,
            houseno=houseno,
            
        )
        order.items.add(*item_ids)

        # After everything is done, send confirmation email to the user
        body = ('Thank you for your order! Your food is being made and will be delivered soon!\n'
                f'Your total: {price}\n'
                'Thank you again for your order!')
        
        # send_mail(
        #     'Thank You For Your Order!',
        #     body,
        #     'example@example.com',
        #     [email],
        #     fail_silently=False
        # )
        
        context = {
            'items': order_items['items'],
            'price': price
        }

        return redirect('order-confirmation', pk=order.pk)

class OrderConfirmation(View):
    def get(self, request, pk, *args, **kwargs):
        order = OrderModel.objects.get(pk=pk)

        context = {
            'pk': order.pk,
            'items': order.items,
            'price': order.price,
        }

        return render(request, 'customer/order_confirmation.html', context)

    def post(self, request, pk, *args, **kwargs):
        data = json.loads(request.body)

        if data['isPaid']:
            order = OrderModel.objects.get(pk=pk)
            order.is_paid = True
            order.save()

        return redirect('payment-confirmation')


class OrderPayConfirmation(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/order_pay_confirmation.html')

class Menu(View):
    def get(self, request, *args, **kwargs):
        menu_items = MenuItem.objects.all()

        context = {
            'menu_items': menu_items
        }

        return render(request, 'customer/menu.html', context)


class MenuSearch(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get("q")

        menu_items = MenuItem.objects.filter(
            Q(name__icontains=query) |
            Q(price__icontains=query) |
            Q(description__icontains=query)
        )

        context = {
            'menu_items': menu_items
        }

        return render(request, 'customer/menu.html', context)