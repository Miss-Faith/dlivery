import json
from django.contrib.auth import authenticate, login
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
    if request.method == 'POST':
        Signupform = SignupForm(request.POST,request.FILES)
        form = LoginForm(request.POST)
        if request.POST.get('submit') == 'Login':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

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
            User.objects.create_user(username=username, email=email, password=password)
            return redirect('menu')
    else:
        Signupform = SignupForm()
        form = LoginForm

    return render(request, 'customer/index.html', {'Signupform': Signupform, 'form':form})


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
        email = request.POST.get('email')
        street = request.POST.get('street')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip')

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
            email=email,
            street=street,
            city=city,
            state=state,
            zip_code=zip_code
        )
        order.items.add(*item_ids)

        # After everything is done, send confirmation email to the user
        body = ('Thank you for your order! Your food is being made and will be delivered soon!\n'
                f'Your total: {price}\n'
                'Thank you again for your order!')
        
        send_mail(
            'Thank You For Your Order!',
            body,
            'example@example.com',
            [email],
            fail_silently=False
        )
        
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