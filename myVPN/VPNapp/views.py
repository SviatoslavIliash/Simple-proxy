from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

import requests
from bs4 import BeautifulSoup
from threading import Lock

from .forms import LoginForm, SignupForm, UserForm, MySiteForm
from .models import MySite
from .utils import *

mutex = Lock()  # Creating mutex object for counting site data properly with multiple threads


def index(request):
    login_form = LoginForm()

    return render(request, "index.html", {'login_form': login_form})


# @csrf_protect
def user_signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, 'Registration Successful! Please Sign In. ')
            return redirect('index')
        else:

            return render(request, "signup.html", {'signup_form': form})

    signup_form = SignupForm()

    return render(request, "signup.html", {'signup_form': signup_form})


@csrf_protect
def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('user_page')
            else:
                messages.error(request, 'Invalid Username or Password')
                return redirect('index')


def user_logout(request):
    logout(request)
    messages.success(request, 'You Were Logged Out!')
    return redirect('index')


@csrf_protect
@login_required
def user_page(request):
    if request.user.is_authenticated:
        if request.method == "POST" and 'user_submit' in request.POST:
            u_form = UserForm(request.POST, request.FILES, instance=request.user)
            if u_form.is_valid():
                u_form.save()
        else:
            u_form = UserForm(instance=request.user)
        if request.method == "POST" and 'new_site_submit' in request.POST:
            site_form = MySiteForm(request.POST)
            if site_form.is_valid():
                site = site_form.save(commit=False)
                site.user = request.user
                site.save()

        site_form = MySiteForm()
        my_sites = MySite.objects.all()

        context = {'user': request.user, 'user_form': u_form, 'site_form': site_form, 'my_sites': my_sites}
        return render(request, "userPage.html", context)

    messages.error(request, 'Login First')
    return redirect('index')


def my_alias_view(request, alias, site_path=''):
    if request.method == "GET":
        my_site = get_object_or_404(MySite, alias=alias)
        '''Add headers'''
        headers = get_headers(request.META)
        params = request.GET.copy()
        headers['ACCEPT-ENCODING'] = 'identity'

        for key in list(headers.keys()):
            if key.lower() == 'content-length':
                del headers[key]

        res = requests.get(my_site.alias_url + '/' + site_path, headers=headers, params=params, stream=True)

        '''Request and Response data volume and visit counter'''
        with mutex:
            my_site = get_object_or_404(MySite, alias=alias)
            my_site.data_out += dict_len(headers)  # volume in B
            my_site.data_in = my_site.data_in + len(res.content) / 1024  # volume in KiB
            if 'content-type' in res.headers and 'text/html' in res.headers['content-type']:
                if res.status_code == 200:
                    my_site.visit_counter = int(my_site.visit_counter) + 1
            my_site.save()

        if 'content-type' in res.headers and 'text/html' in res.headers['content-type']:
            bs = BeautifulSoup(res.text, 'html.parser')
            a_list = bs.findAll("a")
            link_list = bs.findAll("link")
            img_list = bs.findAll("img")
            script_list = bs.findAll("script")

            for a_item in a_list:
                if 'href' in a_item.attrs:
                    a_item['href'] = change_tag(alias, my_site, a_item['href'])

            for link_item in link_list:
                if 'href' in link_item.attrs:
                    link_item['href'] = change_tag(alias, my_site, link_item['href'])

            for img_item in img_list:
                if 'src' in img_item.attrs:
                    img_item['src'] = change_tag(alias, my_site, img_item['src'])

            for script_item in script_list:
                if 'src' in script_item.attrs:
                    script_item['src'] = change_tag(alias, my_site, script_item['src'])

            proxy_response = HttpResponse(str(bs), status=res.status_code)
        else:
            proxy_response = HttpResponse(res.content, status=res.status_code)

        excluded_headers = {'connection', 'keep-alive', 'proxy-authenticate', 'proxy-authorization', 'te', 'trailers',
                            'transfer-encoding', 'upgrade', 'content-encoding', 'content-length'}
        for key, value in res.headers.items():
            if key.lower() in excluded_headers:
                continue
            else:
                proxy_response[key] = value

        return proxy_response

