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

    # if user is searching updating or saving
    if response.method == "POST":

        # if user is searching or updating
        if 'form-search' in response.POST or 'form-update' in response.POST:
            # gets all user inputs
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

            # uses apis to get results
            average, results = get_responses(inputted, all_scales)
            return render(response, "app/home.html", {"inputted": inputted, "results": results, "all_scales": all_scales, "average": average})

        # if user saves a listing
        else:

            if response.user.is_authenticated:
                for element in response.POST:
                    if "{" in element:
                        listing = json.loads(element.replace("'", '"'))
                # attempts to saves listing
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
        # return to current page
                return HttpResponseRedirect(response.path_info)
        return HttpResponseRedirect(response.path_info)

    # if loading page for first time
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
    # checks if logged in
    if response.user.is_authenticated:
        # get user from database
        current_user = User.objects.get(id=response.user.id)
        form = update_user_details_form(
            response.POST or None, instance=current_user)
        # checks if form was submitted and valid
        if form.is_valid():
            # saves info
            form.save()
            login(response, current_user,
                  backend='django.contrib.auth.backends.ModelBackend')
            messages.success(response, "Information updated")
        elif response.method == "POST":
            messages.success(response, "Information unable to be updated")
        # calls page with settings when logged in
        return render(response, "app/settings.html", {"form": form})
    # return page when not logged in
    else:
        return render(response, "app/settings.html", {})


def saved(response):
    listings = {
    }

    # checks if user is save deleting or updating there saved listing
    if response.method == "POST":

        # if save then gets wanted price and updates database
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

        # if delete then removes form database
        elif "delete" in list(response.POST.keys())[-1]:
            user_saved.objects.get(user=response.user, listing=listing.objects.get(
                id=int(list(response.POST)[-1].replace(" delete", "")))).delete()
            messages.success(response, "Listing deleted")

        # gets all saved and adds to dict and sorts
        saved = user_saved.objects.filter(user=response.user).values()
        for save in saved:
            listings[listing.objects.get(pk=save.get("listing_id")).id] = listing.objects.get(
                pk=save.get("listing_id")).__dict__
            listings[listing.objects.get(pk=save.get(
                "listing_id")).id]["wanted_price"] = save["wanted_price"]
    else:
        # gets all saved and adds to dict and sorts
        saved = user_saved.objects.filter(user=response.user).values()
        for save in saved:
            listings[listing.objects.get(pk=save.get("listing_id")).id] = listing.objects.get(
                pk=save.get("listing_id")).__dict__
            listings[listing.objects.get(pk=save.get(
                "listing_id")).id]["wanted_price"] = save["wanted_price"]
    # returns page with data
    return render(response, "app/saved.html", {"listings": listings})


def login_page(response):
    # check if user trying to login
    if response.method == "POST":
        username = response.POST["username"]
        password = response.POST["password"]
        # checks if username and password exits and match in database
        user = authenticate(response, username=username, password=password)
        if user is not None:
            # if user is valid the log in user
            login(response, user)
            messages.success(response, "Logged in")
            return redirect("/")
        else:
            # if invalid login
            messages.success(response, "There was an error login")
            return render(response, "app/login.html", {})
    # if not return page for login
    else:
        return render(response, "app/login.html", {})


def signup(response):
    # checks if user is trying to signup
    if response.method == "POST":
        form = create_user_form(response.POST)
        # checks if user input is valid
        if form.is_valid():
            # adds user to database
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
    # creates blank form and returns page to user
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
    # checks if listing exists in the database
    if not listing.objects.filter(url=wanted_listing["url"]).exists():
        # if doesnt exist then it creates a new entry into the database
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
        # if exists gen get for database
        save_listing = listing.objects.all().filter(url=wanted_listing["url"])
    # checks if already link between user and listing
    if not user_saved.objects.filter(user=response.user, listing=save_listing[0]).exists():
        # creates new database entry
        user_saved.objects.create(
            user=response.user, listing=save_listing[0], wanted_price=-1)
        return True
    # doesnt update database
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
        mergesort(results, 0, len(results)-1, "price")
    elif inputted["sorting_method"] == "customer review":
        mergesort(results, 0, len(results)-1, "review")

    def merge(arr, start, mid, end, attribute):
        start2 = mid + 1
        if getattr(arr[mid], attribute) <= getattr(arr[start2], attribute):
            return

        while (start <= mid and start2 <= end):

            if getattr(arr[start], attribute) <= getattr(arr[start2], attribute):
                start += 1
            else:
                value = arr[start2]
                index = start2

                while (index != start):
                    arr[index] = arr[index - 1]
                    index -= 1

                arr[start] = value
                start += 1
                mid += 1
                start2 += 1

    def mergesort(array, left, right, attribute):
        if (left < right):
            middle = left + (right - left) // 2
            mergesort(array, left, middle, attribute)
            mergesort(array, middle + 1, right, attribute)
            merge(array, left, middle, right, attribute)

    mergesort(results, 0, len(results)-1, "price")

    mergesort(results, 0, len(results)-1, "shipping")

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
