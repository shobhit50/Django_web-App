from django.shortcuts import render , redirect
from django.http import HttpResponse
from .models import Listing, userdata, Review
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User 
from django.contrib.auth import get_user_model

from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.shortcuts import get_object_or_404
from cloudinary.uploader import upload
import cloudinary.api
from django.db.models import Q



User = get_user_model()




#test 



def search(request):
    listings_data = Listing.objects.all()
    listings_data = count_review(request,listings_data)
    if request.method == 'POST':
        search_item = request.POST.get('search', '')
        price_filter = ''
        rating_filter = ''
        choice = request.POST.get('price', '')
        if choice in ('low_to_high', 'high_to_low'):
            print('done')
            price_filter = choice
        else:
            print('not done')
            rating_filter = choice

        if search_item:
            listings_data = listings_data.filter(
                Q(location__icontains=search_item) |
                Q(price__icontains=search_item) |
                Q(country__icontains=search_item)
            )

        if price_filter:
            print('price working',price_filter)
            if price_filter == 'low_to_high':
                listings_data = listings_data.order_by('price')
            elif price_filter == 'high_to_low':
                listings_data = listings_data.order_by('-price')
        if rating_filter:
            print('rating working',rating_filter)
            listings_data = count_review(request,listings_data)
            if rating_filter == 'top_to_low':
                listings_data = sorted(listings_data, key=lambda x: x.avg, reverse=True)
            elif rating_filter == 'low_to_top':
                listings_data = sorted(listings_data, key=lambda x: x.avg, reverse=False)
    listings_data = count_review(request,listings_data)

    # listings_data = sorted(listings_data, key=lambda x: x.avg, reverse=True)
    return render(request, 'myfirst_app/listings/index.html', {'listings_data': listings_data })

def count_review(request,listings_data):
        listings_data = listings_data
        for listing in listings_data:
            avg = 0
            total_reviews = listing.reviews.count()
            if total_reviews > 0:
                avg = sum(review.rating for review in listing.reviews.all()) / total_reviews
                avg = round(avg, 2)

            # Dynamically add avg as an attribute to the instance
            setattr(listing, 'avg', avg)
        return listings_data



# Create your views here.
def index(request):
    listings_data = Listing.objects.all()
    listings_data = count_review(request,listings_data)
    # for listing in listings_data:
    #     avg = 0
    #     total_reviews = listing.reviews.count()
    #     if total_reviews > 0:
    #         avg = sum(review.rating for review in listing.reviews.all()) / total_reviews
    #         avg = round(avg, 2)

    #     # Dynamically add avg as an attribute to the instance
    #     setattr(listing, 'avg', avg)
    return render(request, 'myfirst_app/listings/index.html', {'listings_data': listings_data })

# -----------------------------------------------------------------------------------------------------------
# create new listing
def new(request):
    if not islogin(request):
        return redirect('loginform')
    else:
        print(request.user)
        return render(request, 'myfirst_app/listings/new.html')
        

# new listing get data
def newPost(request):
    if not islogin(request):
        return redirect('loginform')
    if request.method == 'POST':
        try:
            title = request.POST['title']
            description = request.POST['description']
            #here we will upload image to cloudinary
            image_url=image_upload(request)
            #here we will save the image url in cloud database
            price = request.POST['price']
            country = request.POST['country']
            location = request.POST['location']
            current_user = request.user
            new_listing = Listing(title=title,description=description,image_url=image_url,
                                  price=price,location=location,country=country,owner=current_user)
            new_listing.save()
            messages.success(request, 'new listing created successfully')
            return render(request, 'myfirst_app/listings/index.html')

        except Exception as e:
            print(f"Error creating user: {e}")
            raise
# -----------------------------------------------------------------------------------------------------------
    #show listing
        
def show(request, listing_id):
        listing = get_object_or_404(Listing, pk=listing_id)
        avg = 0
        total_reviews = len(listing.reviews.all())
        if total_reviews > 0:
            for review in listing.reviews.all():
                avg += review.rating
                time = review.createdAt.strftime("%Y-%m-%d %H:%M")
                setattr(review, 'time', time)
                setattr(listing, 'review', review)
                print (listing.review.time)
            avg = avg / total_reviews
            avg = round(avg, 2)
           
        else:
            avg = 0
        print(avg)
        return render(request, 'myfirst_app/listings/show.html', {'listing': listing, 'avg': avg})
#edit listing
def edit(request, listing_id):
    if not islogin(request):
        return redirect('loginform')
    listing = get_object_or_404(Listing, pk=listing_id)
    return render(request, 'myfirst_app/listings/edit.html', {'listing': listing})

#update listing
def update(request, listing_id):
    if not islogin(request):
        return redirect('loginform')
    if request.method == 'POST':
        listing = get_object_or_404(Listing, pk=listing_id)
        listing.title = request.POST['title']
        listing.description = request.POST['description']

        listing.image_url = image_upload(request)
        # listing.image_url = "https://images.unsplash.com/photo-1566073771259-6a8506099945?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8aG90ZWxzfGVufDB8fDB8fHww&auto=format&fit=crop&w=800&q=60"
        listing.price = request.POST['price']
        listing.country = request.POST['country']
        listing.location = request.POST['location']
        listing.save()
        messages.success(request, 'listing updated successfully')
        return redirect('index')
    return render(request, 'myfirst_app/listings/show.html', {'listing': listing})

#delete listing
def delete(request, listing_id):
    if not islogin(request):
        return redirect('loginform')
    if request.method == 'POST':
        listing = get_object_or_404(Listing, pk=listing_id)
        image_CL = listing.image_url
        listing.delete_associated_reviews()
        listing.delete()
        result = image_delete(request,image_CL)
        messages.success(request, 'listing deleted successfully')
        return redirect('index')
    return render(request, 'myfirst_app/listings/show.html', {'listing': listing})

 # -----------------------------------------------------------------------------------------------------------
#rewrite listing

def Reviews(request, listing_id):
    if not islogin(request):
        return redirect('loginform')
    if request.method == 'POST':
        listing = get_object_or_404(Listing, pk=listing_id)
        #it is a object of rewiew
        
        comment = request.POST.get('review[comment]')
        rating = request.POST.get('review[rating]')
        rating = int(rating)
        # review_user = request.user
        review = Review(comment=comment, rating=rating, user=request.user)
        # # Add the review to the listing's reviews
        review.save()
        listing.reviews.add(review)
        # listing.price = listing.price.to_decimal()
        listing.save()
        
        
    messages.success(request, 'Review added successfully')
    return render(request, 'myfirst_app/listings/show.html', {'listing': listing})
#delete Review

def deleteReview(request, listing_id, review_id):
    if not islogin(request):
        return redirect('loginform')
    if request.method == 'POST':
        listing = get_object_or_404(Listing, pk=listing_id)
        review = get_object_or_404(Review, pk=review_id)
        listing.reviews.remove(review)
        review.delete()
    messages.success(request, 'Review deleted successfully')
    return render(request, 'myfirst_app/listings/show.html', {'listing': listing})


# singup form
def singup(request):
    return render(request, 'myfirst_app/user/singup.html')
# create new user
def createUser(request):
    if request.method == 'POST':
        try:
            userName = request.POST['username']
            userMail = request.POST['email']
            userPass = request.POST['password']

            # create user
            new_user = User.objects.create_user(username=userName, email=userMail, password=userPass)
            # print(user)
            messages.success(request, 'new user created successfully now you can login')
            return redirect('index')

        except Exception as e:
            print(f"Error creating user: {e}")
            raise  # Re-raise the exception for better debugging
# -----------------------------------------------------------------------------------------------------------
# login form
def loginform(request):
    return render(request, 'myfirst_app/user/login.html')
# login user
def loginHandler(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        if not isuserExist(request, username):
            messages.warning(request, 'User not exist')
            return redirect('loginform')
        try:
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'You are now logged in')
                return redirect('index')
            else:
                messages.warning(request, 'Wrong password')
                return redirect('loginform')
        except (KeyError, TypeError) as e:
            print(f"Error during login: {e}")
            return redirect('loginform')

    return redirect('loginform')

#Change Password
def changePassword(request):
    if request.method == 'POST':
        if not isuserExist(request, request.POST['username']):
            messages.warning(request, 'User not exist')
            return render(request, 'myfirst_app/user/changePassword.html')
        try:
            userName = request.POST.get('username').strip()
            userPassOld = request.POST['Old_password']
            userPassNew = request.POST['new_password']
            user = User.objects.get(username=userName)
            password_matches = check_password(userPassOld, user.password)
            if password_matches:
                user.set_password(userPassNew)
                user.save()
                messages.success(request, 'Password changed successfully now you can login')
                return redirect('loginform')
        except Exception as e:
            print(f"Error creating user: {e}")
            raise 
    return render(request, 'myfirst_app/user/changePassword.html')

def logoutHandler(request):
    logout(request)
    messages.success(request, 'You are now logged out')
    return redirect('index')


# -----------------------------------------------------------------------------------------------------------

def form(request):
    return HttpResponse("Hello, world. You're at the polls index.")

#---------------------------------------------------------------------------------------
#all mideleware here
def islogin(request):
    return request.user.is_authenticated

def isuserExist(request, username):
    return User.objects.filter(username=username)


#cludinary image upload midelware
def image_upload(request):
    if request.method == 'POST':
        try:
            #here we will upload image to cloudinary
            image_file = request.FILES['image']
            image_file = image_file.read()
            result = upload(image_file)
            cloudinary_url = result['secure_url']
            #here we will save the image url in cloud database
            image_url=cloudinary_url
            return image_url
        except Exception as e:
            print(f"Error creating user: {e}")
            raise
    

 #cloudinary image delete midelware
def image_delete(request,data):
    if request.method == 'POST':
        try:
            image_CL = data
            public_id = image_CL.split('/')[-1].split('.')[0]
            result = cloudinary.uploader.destroy(public_id, invalidate=True)
            return result
        except Exception as e:
            print(f"Error creating user: {e}")
            raise
            