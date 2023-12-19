from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import create_user_form, update_user_details_form
from django.contrib.auth.models import User
from app.models import user_saved, listing
from django.http import HttpResponseRedirect
import json
import requests
import operator


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

        if 'form-search' in response.POST or 'form-update' in response.POST:
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

            average, results = get_responses(inputted, all_scales)
            return render(response, "app/home.html", {"inputted": inputted, "results": results, "all_scales": all_scales, "average": average})

        else:

            if response.user.is_authenticated:
                for element in response.POST:
                    if "{" in element:
                        listing = json.loads(element.replace("'", '"'))
                done = save_listing(response, listing)
                results = None
                average = "-"
                if done:
                    messages.success(response, "Your listing has been saved.")
                else:
                    messages.success(
                        response, "Listing couldn't be save. This may be due to you already having it <a href='/saved'>saved</a>.")
            else:
                messages.success(
                    response, "You need to <a href='/login'>login</a> to save a result.")
                results = None
                average = "-"
                return HttpResponseRedirect(response.path_info)
        return HttpResponseRedirect(response.path_info)

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
        return render(response, "app/home.html", {"inputted": inputted, "all_scales": all_scales, "average": "-"})


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
    listings = {
    }

    if response.method == "POST":

        if "save" in list(response.POST.keys())[-1]:
            new_wanted_price = response.POST["wanted_price"]
            if new_wanted_price in ["none", "None", 0, "0"]:
                new_wanted_price = -1
            else:
                new_wanted_price = int(new_wanted_price)

            updated_listing = user_saved.objects.get(listing=listing.objects.get(
                id=int(list(response.POST)[-1].replace(" save", ""))))
            updated_listing.wanted_price = new_wanted_price
            updated_listing.save()

        elif "delete" in list(response.POST.keys())[-1]:
            user_saved.objects.get(user=response.user, listing=listing.objects.get(
                id=int(list(response.POST)[-1].replace(" delete", "")))).delete()
            messages.success(response, "Listing deleted")

        saved = user_saved.objects.filter(user=response.user).values()
        for save in saved:
            listings[listing.objects.get(pk=save.get("listing_id")).id] = listing.objects.get(
                pk=save.get("listing_id")).__dict__
            listings[listing.objects.get(pk=save.get(
                "listing_id")).id]["wanted_price"] = save["wanted_price"]
    else:
        saved = user_saved.objects.filter(user=response.user).values()
        for save in saved:
            listings[listing.objects.get(pk=save.get("listing_id")).id] = listing.objects.get(
                pk=save.get("listing_id")).__dict__
            listings[listing.objects.get(pk=save.get(
                "listing_id")).id]["wanted_price"] = save["wanted_price"]
    return render(response, "app/saved.html", {"listings": listings})


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


def save_listing(response, wanted_listing):
    if not listing.objects.filter(url=wanted_listing["url"]).exists():
        save_listing = [listing.objects.create(
            name=wanted_listing["name"],
            price=wanted_listing["price"],
            shipping=wanted_listing["shipping_cost"],
            currency=wanted_listing["currency"],
            url=wanted_listing["url"],
            location=wanted_listing["location"],
            image=wanted_listing["image"],
            review=wanted_listing["review"],
            website=wanted_listing["website"],
            condition=wanted_listing["condition"])]
    else:
        save_listing = listing.objects.all().filter(url=wanted_listing["url"])
    if not user_saved.objects.filter(user=response.user, listing=save_listing[0]).exists():
        user_saved.objects.create(
            user=response.user, listing=save_listing[0], wanted_price=-1)
        return True
    else:
        return False


def get_responses(inputted, all_scales):
    Ebay_number_of_returns = 7
    Amazon_number_of_returns = 7
    results_class_list = []
    results = []
    search = inputted["search"]
    for i in all_scales:
        if dict(all_scales.get(i)).get('on') == 'on':
            search += " "+i

    # ebay
    ebay_params = {
        'api_key': '728A2816A69F498D85B6EDA746D9153B',
        'ebay_domain': 'ebay.co.uk',
        'search_term': search,
        'type': 'search'
    }

    ebay_results = requests.get(
        'https://api.countdownapi.com/request', ebay_params).json().get('search_results')

    for i in range(Ebay_number_of_returns):
        try:
            condition = "unknown"
            if ebay_results[i].get("condition") == "Brand New":
                condition = "new"
            if ebay_results[i].get("condition") == "Used":
                condition = "used"
            results_class_list.append(result_class(
                ebay_results[i].get('title'),
                ebay_results[i].get('price').get('value'),
                0,
                "GBP",
                ebay_results[i].get('link'),
                "None",
                ebay_results[i].get('image'),
                ebay_results[i].get('seller_info').get(
                    "positive_feedback_percent"),
                "Ebay",
                condition
            ))
        except:
            pass

    # amazon
    amazon_params = {
        'api_key': '5A6709D3BB1C4232BB93E0955F9934BD',
        'type': 'search',
        'amazon_domain': 'amazon.com',
        'search_term': search,
        'output': 'json',
        'page': '1'
    }

    amazon_results = requests.get(
        'https://api.asindataapi.com/request', amazon_params).json().get('search_results')
    for i in range(Amazon_number_of_returns):
        try:
            results_class_list.append(result_class(
                amazon_results[i].get('title'),
                amazon_results[i].get('price').get('value'),
                0,
                amazon_results[i].get('price').get('currency'),
                "/".join(amazon_results[i].get('link').split("/")[0:6]),
                "None",
                amazon_results[i].get('image'),
                0,
                "Amazon",
                "New"
            ))
        except:
            pass

    # filtering
    # price
    results_class_list_copy = results_class_list.copy()
    if inputted["min_price"] != '':
        for response in results_class_list_copy:
            if float(response.price) < float(inputted["min_price"]):
                results_class_list.remove(response)
    if inputted["max_price"] != '':
        for response in results_class_list_copy:
            if float(response.price) > float(inputted["max_price"]):
                results_class_list.remove(response)
    # condition
    if inputted["new"] != '' or inputted["used"] != '' or inputted["unknown"] != '':
        temp = []
        for response in results_class_list:
            if response.condition == "new" and inputted["new"] != '':
                temp.append(response)
            elif response.condition == "used" and inputted["used"] != '':
                temp.append(response)
            elif response.condition == "unknown" and inputted["unknown"] != '':
                temp.append(response)
            else:
                temp.append(response)
        results_class_list = temp.copy()

    # sorting
    if inputted["sorting_method"] == "none":
        pass
    elif inputted["sorting_method"] == "price":
        results_class_list = sorted(
            results_class_list, key=lambda x: float(x.price))
    elif inputted["sorting_method"] == "customer review":
        results_class_list = sorted(
            results_class_list, key=lambda x: float(x.review))

    for result in results_class_list:
        results.append(result.get_dict())

    try:
        average = 0
        for result in results_class_list:
            average += float(result.price)
        average /= len(results_class_list)
        average = ("%.2f" % float(average))
    except:
        average = "-"

    return average, results


class result_class():
    def __init__(self, name, price, shipping_cost, currency, url, location, image, review, website, condition):
        self.name = name
        self.price = ("%.2f" % float(price))
        self.shipping_cost = ("%.2f" % float(shipping_cost))
        self.currency = currency
        self.url = url
        self.location = location
        self.image = image
        self.review = int(review)
        self.website = website
        self.condition = condition

    def get_dict(self):
        return {"name": self.name, "price": self.price, "shipping_cost": self.shipping_cost, "currency": self.currency, "url": self.url, "location": self.location, "image": self.image, "review": self.review, "website": self.website, "condition": self.condition}

    def display(self):
        print("name", self.name, "price", self.price, "shipping_cost", self.shipping_cost, "currency", self.currency, "url", self.url,
              "location", self.location, "image", self.image, "review", self.review, "website", self.website, "condition", self.condition)
