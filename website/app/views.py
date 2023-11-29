from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import create_user_form, update_user_details_form
from django.contrib.auth.models import User

from ebaysdk.exception import ConnectionError
from ebaysdk.finding import Connection
import json


# Create your views here.


def home(response):
    all_sorting_method = ["none", "price",
                          "customer review", "newest first"]
    all_scales = {"N Gauge (1:148)": 'n_gauge',
                  "TT Gauge (1:120)": 'tt_gauge',
                  "OO9 Gauge (1:76)": 'oo9_gauge',
                  "OO/HO Gauge (1:76)": 'oo_gauge',
                  "O Gauge (1:43)": 'o_gauge',
                  "G Gauge (1:22.5)": 'g_gauge',
                  }

    if response.method == "POST":
        search = response.POST['search']
        min_price = response.POST['min_price']
        max_price = response.POST['max_price']
        new = "".join(response.POST.getlist('new'))
        used = "".join(response.POST.getlist('used'))
        unknown = "".join(response.POST.getlist('unknown'))
        n_gauge = "".join(response.POST.getlist('n_gauge'))
        tt_gauge = "".join(response.POST.getlist('tt_gauge'))
        oo9_gauge = "".join(response.POST.getlist('oo9_gauge'))
        oo_gauge = "".join(response.POST.getlist('oo_gauge'))
        o_gauge = "".join(response.POST.getlist('o_gauge'))
        g_gauge = "".join(response.POST.getlist('g_gauge'))
        sorting_method = response.POST['sorting_method']
        all_sorting_method.remove(sorting_method)

        inputted = {"search": search,
                    "min_price": min_price,
                    "max_price": max_price,
                    "new": new,
                    "used": used,
                    "unknown": unknown,
                    "sorting_method": sorting_method,
                    "all_sorting_method": all_sorting_method, }

        all_scales = {"N Gauge (1:148)": {"on": n_gauge, "id": "n_gauge"},
                      "TT Gauge (1:120)": {"on": tt_gauge, "id": "tt_gauge"},
                      "OO9 Gauge (1:76)": {"on": oo9_gauge, "id": "oo9_gauge"},
                      "OO/HO Gauge (1:76)": {"on": oo_gauge, "id": "oo_gauge"},
                      "O Gauge (1:43)": {"on": o_gauge, "id": "o_gauge"},
                      "G Gauge (1:22.5)": {"on": g_gauge, "id": "g_gauge"},
                      }

        if inputted["search"] == "":
            results = None
        else:
            results = get_responses(inputted, all_scales)
        return render(response, "app/home.html", {"inputted": inputted, "results": results, "all_scales": all_scales})
    else:
        all_sorting_method.remove("none")

        inputted = {"search": "",
                    "min_price": "",
                    "max_price": "",
                    "new": "",
                    "used": "",
                    "unknown": "",
                    "n_gauge": "",
                    "tt_gauge": "",
                    "oo9_gauge": "",
                    "oo_gauge": "",
                    "o_gauge": "",
                    "g_gauge": "",
                    "sorting_method": "none",
                    "all_sorting_method": all_sorting_method,
                    "all_scales": all_scales}
        results = {}
        return render(response, "app/home.html", {"inputted": inputted, "all_scales": all_scales})


def settings(response):
    if response.user.is_authenticated:
        current_user = User.objects.get(id=response.user.id)
        form = update_user_details_form(
            response.POST or None, instance=current_user)
        if form.is_valid():
            form.save()
            login(response, current_user,
                  backend='django.contrib.auth.backends.ModelBackend')
            messages.success(response, "Information updated")
        elif response.method == "POST":
            messages.success(response, "Information unable to be updated")

        return render(response, "app/settings.html", {"form": form})

    else:
        return render(response, "app/settings.html", {})


def saved(response):
    return render(response, "app/saved.html", {})


def login_page(response):
    if response.method == "POST":
        username = response.POST["username"]
        password = response.POST["password"]
        user = authenticate(response, username=username, password=password)
        if user is not None:
            login(response, user)
            messages.success(response, "Logged in")
            return redirect("/")
        else:
            messages.success(response, "There was an error login")
            return render(response, "app/login.html", {})
    else:
        return render(response, "app/login.html", {})


def signup(response):
    if response.method == "POST":
        form = create_user_form(response.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = authenticate(username=username, password=password)
            login(response, user)
            messages.success(response, "Sign up successful and logged in")
            return redirect("/")
        else:
            messages.success(response, "Sign up unsuccessful")
            return render(response, "app/signup.html", {"form": form})

    else:
        form = create_user_form()
        return render(response, "app/signup.html", {"form": form})


def logout_user(response):
    logout(response)
    messages.success(response, "Logged out")
    return redirect("/")


def redirect_home_1(response):
    messages.success(response, "Email sent")
    return redirect("/")


def redirect_home_2(response):
    messages.success(response, "Password changed")
    return redirect("/")


def delete_account(response):
    current_user = User.objects.get(id=response.user.id)
    current_user.delete()
    messages.success(response, "Account Deleted")
    return redirect("/")


def get_responses(inputted, all_scales):
    Ebay_number_of_returns = 1
    results_class_list = []
    results = {}
    print(inputted)

    ebay_filters = []

    api = Connection(domain='svcs.sandbox.ebay.com',
                     appid='HenryOwe-NEA-SBX-2ac348da7-f6ef1a16', config_file=None)
    request = {
        'keywords': inputted["search"],
        'itemFilter': ebay_filters,
        'paginationInput': {
            'entriesPerPage': Ebay_number_of_returns,
            'pageNumber': 1
        },
        'sortOrder': 'PricePlusShippingLowest',
    }

    response = json.loads(api.execute(
        'findItemsAdvanced', request).json()).get("searchResult").get("item")

    for item in response:
        results_class_list.append(result_class(
            item.get("title"),
            item.get("sellingStatus").get("currentPrice").get("value"),
            item.get("shippingInfo").get("shippingServiceCost").get("value"),
            item.get("sellingStatus").get("currentPrice").get("_currencyId"),
            item.get("viewItemURL"),
            item.get("location"),
            item.get("viewItemURL"),
            "ebay"))

    for result in results_class_list:
        results[""] = result.get_dict()

    return results


class result_class():
    def __init__(self, name, price, shipping_cost, currency, url, location, image, website):
        self.name = name
        self.price = price
        self.shipping_cost = shipping_cost
        self.currency = currency
        self.url = url
        self.location = location
        self.image = image
        self.website = website

    def get_dict(self):
        return {"name": self.name, "price": self.price, "shipping_cost": self.shipping_cost, "url": self.url, "location": self.location, "image": self.image, "website": self.website}

    def display(self):
        print("name:", self.name, "price:", self.price, "shipping_cost:", self.shipping_cost, "url:",
              self.url, "location:", self.location, "image:", self.image, "website:", self.website)
