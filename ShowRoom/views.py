from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Q
from .forms import *
from .models import *
from django.template import *
t = Template("{{ request.META.HTTP_REFERER }}")
from django.http import HttpRequest
req = HttpRequest()
req.META

# Create your views here.
title='Mobile Show Room '

def home(request):
    userType="Guest"
    loginId="Guest"
    userId=0
    wlCount=0
    if request.session.get('USER_LOGIN_ID') is not None:
        userType=format(request.session.get('USER_TYPE'))
        loginId=format(request.session.get('USER_LOGIN_ID'))
        userId=format(request.session.get('USER_ID'))
        wlCount=WishList.objects.filter(user=userId).count()
    page='Home'
    sub_page='Home'
    pgTitle=title+' | '+page
    brands = Brand.objects.all()
    records = Mobile.objects.all()
    context={'brands':brands,'records':records,'page':page,'sub_page':sub_page,'pgTitle':pgTitle,'userType':userType,'loginId':loginId,'wlCount':wlCount}
    return render(request,'ShowRoom/home.html',context)

def search(request):
    userType="Guest"
    loginId="Guest"
    userId=0
    wlCount=0
    if request.session.get('USER_LOGIN_ID') is not None:
        userType=format(request.session.get('USER_TYPE'))
        loginId=format(request.session.get('USER_LOGIN_ID'))
        userId=format(request.session.get('USER_ID'))
        wlCount=WishList.objects.filter(user=userId).count()
    page='Search'
    sub_page='Search'
    pgTitle=title+' | '+page
    brands=Brand.objects.all()
    records = []
    brand = request.GET.get('brand') if request.GET.get('brand') != None else ''
    os = request.GET.get('os') if request.GET.get('os') != None else ''
    minamount = int(request.GET.get('minamount')) if request.GET.get('minamount') != None else 0
    maxamount = int(request.GET.get('maxamount')) if request.GET.get('maxamount') != None else 0
    minP=5000
    maxP=1500000;
    if brand:
        records = Mobile.objects.filter (Q(brand__name__icontains=brand))
    if os:
        records = Mobile.objects.filter (Q(os__contains=os))
    if maxamount > 0:
        minP=minamount
        maxP=maxamount
        records = Mobile.objects.filter (Q(price__lte=maxamount) & Q(price__gte=minamount))
    context={'minP':minP,'maxP':maxP,'records':records,'brands':brands,'page':page,'sub_page':sub_page,'pgTitle':pgTitle,'userType':userType,'loginId':loginId,'wlCount':wlCount}
    return render(request,'ShowRoom/search.html',context)

def compare(request):
    userType="Guest"
    loginId="Guest"
    userId=0
    wlCount=0
    if request.session.get('USER_LOGIN_ID') is not None:
        userType=format(request.session.get('USER_TYPE'))
        loginId=format(request.session.get('USER_LOGIN_ID'))
        userId=format(request.session.get('USER_ID'))
        wlCount=WishList.objects.filter(user=userId).count()
    page='Compare'
    sub_page='Compare'
    pgTitle=title+' | '+page
    brands=Brand.objects.all()
    minP=5000
    maxP=1500000;
    id1 = int(request.session.get('COMP1')) if request.session.get('COMP1') != None else 0
    id2 = int(request.session.get('COMP2')) if request.session.get('COMP2') != None else 0
    id3 = int(request.session.get('COMP3')) if request.session.get('COMP3') != None else 0
    rec1 = None
    if id1 > 0:
        rec1=Mobile.objects.get(pk=id1)
    rec2=None
    if id2 > 0:
        rec2=Mobile.objects.get(pk=id2)
    rec3=None
    if id3 >0:
        rec3=Mobile.objects.get(pk=id3)

    context={'rec1':rec1,'rec2':rec2,'rec3':rec3,'minP':minP,'maxP':maxP,'brands':brands,'page':page,'sub_page':sub_page,'pgTitle':pgTitle,'userType':userType,'loginId':loginId,'wlCount':wlCount}
    return render(request,'ShowRoom/compare.html',context)

def wishlist(request):
    userType="Guest"
    loginId="Guest"
    userId=0
    wlCount=0
    if request.session.get('USER_LOGIN_ID') is not None:
        userType=format(request.session.get('USER_TYPE'))
        loginId=format(request.session.get('USER_LOGIN_ID'))
        userId=format(request.session.get('USER_ID'))
        wlCount=WishList.objects.filter(user=userId).count()
    page='Wishlist'
    sub_page='Wishlist'
    pgTitle=title+' | '+page
    records = WishList.objects.filter(Q(user=userId))
    context={'records':records,'page':page,'sub_page':sub_page,'pgTitle':pgTitle,'userType':userType,'loginId':loginId,'wlCount':wlCount}
    return render(request,'ShowRoom/wishlist.html',context)

def removeWishList(request,pk):
    if request.session.get('USER_LOGIN_ID') is not None:
        rec=WishList.objects.filter(id=pk)
        if rec:
            WishList.objects.filter(id=pk).delete()
            messages.success(request, "Item deleted from wishlist")
        else:
            messages.error(request, "Item does not exists")
    else:
        messages.success(request, "Please login/register to manage wishlist.")
    return redirect(request.META['HTTP_REFERER'])

def addToCompare(request,pk):
    added=0
    if request.session.get('COMP1') is not None:
        if request.session.get('COMP1')==pk:
            added=-1
    if request.session.get('COMP2') is not None:
        if request.session.get('COMP2')==pk:
            added=-1
    if request.session.get('COMP3') is not None:
        if request.session.get('COMP3')==pk:
            added=-1
    if request.session.get('COMP1') is None:
        if added==0:
            request.session['COMP1']=pk;
            added=1
    elif request.session.get('COMP2') is None:
        if added==0:
            request.session['COMP2']=pk;
            added=2
    elif request.session.get('COMP3') is None:
        if added==0:
            request.session['COMP3']=pk;
            added=3
    if added == 0:
        messages.error(request, "Compare list is complete, please remove one to add new.")
    elif added == -1:
        messages.error(request, "Item already exists in the list.")
    else:
        messages.success(request, "Item added to compare list at # "+str(added))
    return redirect(request.META['HTTP_REFERER'])

def remFromCompare(request,pk):
    rem=0
    pk = int(pk)
    if pk == 1:
        request.session.pop("COMP1", None)
        rem=1
    elif pk == 2:
        request.session.pop("COMP2", None)
        rem=2
    elif pk==3:
        request.session.pop("COMP3", None)
        rem=3
    if rem == 0:
        messages.error(request, "Nothing removed.")
    else:
        messages.success(request, "Item removed from the compare list.")
    return redirect(request.META['HTTP_REFERER'])

def addToWishList(request,pk):
    if request.session.get('USER_LOGIN_ID') is not None:
        uid=format(request.session.get('USER_ID'))
        u=User.objects.get(id=uid)
        m=Mobile.objects.get(id=pk)
        rec=WishList.objects.filter(Q(mobile=pk) & Q(user=u))
        if rec:
            messages.error(request, "Item already exists in wishlist")
        else:
            wl=WishList();
            wl.user=u
            wl.mobile=m
            wl.save()
            messages.success(request, "Added to wishlist Successfully")
    else:
        messages.error(request, "Please login/register to add in wishlist.")
    return redirect(request.META['HTTP_REFERER'])

def products(request):
    userType="Guest"
    loginId="Guest"
    userId=0
    wlCount=0
    if request.session.get('USER_LOGIN_ID') is not None:
        userType=format(request.session.get('USER_TYPE'))
        loginId=format(request.session.get('USER_LOGIN_ID'))
        userId=format(request.session.get('USER_ID'))
        wlCount=WishList.objects.filter(user=userId).count()
    page='Products'
    sub_page='Products'
    pgTitle=title+' | '+page
    records=Mobile.objects.all()
    context={'records':records,'page':page,'sub_page':sub_page,'pgTitle':pgTitle,'userType':userType,'loginId':loginId,'wlCount':wlCount}
    return render(request,'ShowRoom/products.html',context)

def addMobile(request):
    userType="Guest"
    loginId="Guest"
    userId=0
    wlCount=0
    if request.session.get('USER_LOGIN_ID') is not None:
        userType=format(request.session.get('USER_TYPE'))
        loginId=format(request.session.get('USER_LOGIN_ID'))
        userId=format(request.session.get('USER_ID'))
        wlCount=WishList.objects.filter(user=userId).count()
    page='Products'
    sub_page='Add Mobile'
    pgTitle=title+' | '+page
    form=MobileForm()
    if request.method == 'POST':
        form=MobileForm(request.POST)
        if form.is_valid():            
            form.save()
            messages.success(request, "Mobile Record Added.")
            return redirect('products')
        else:
            messages.error(request, "Some unknown error")

    context={'form':form,'page':page,'sub_page':sub_page,'pgTitle':pgTitle,'userType':userType,'loginId':loginId,'wlCount':wlCount}
    return render(request,'ShowRoom/mobile-form.html',context)

def updateMobile(request,pk):
    userType="Guest"
    loginId="Guest"
    userId=0
    wlCount=0
    if request.session.get('USER_LOGIN_ID') is not None:
        userType=format(request.session.get('USER_TYPE'))
        loginId=format(request.session.get('USER_LOGIN_ID'))
        userId=format(request.session.get('USER_ID'))
        wlCount=WishList.objects.filter(user=userId).count()
    page='Products'
    sub_page='Update Mobile'
    pgTitle=title+' | '+page
    brand=Mobile.objects.get(id=pk)
    form=MobileForm(instance=brand)
    if request.method == 'POST':
        form=MobileForm(request.POST,instance=brand)
        if form.is_valid():
            form.save()
            messages.success(request, "Mobile details updated.")
            return redirect('products')
        else:
            messages.error(request, "Some unknown error")

    context={'form':form, 'page':page,'sub_page':sub_page,'pgTitle':pgTitle,'userType':userType,'loginId':loginId,'wlCount':wlCount}
    return render(request,'ShowRoom/mobile-form.html',context)

def uploadMobilePhoto(request,pk):
    userType="Guest"
    loginId="Guest"
    userId=0
    wlCount=0
    if request.session.get('USER_LOGIN_ID') is not None:
        userType=format(request.session.get('USER_TYPE'))
        loginId=format(request.session.get('USER_LOGIN_ID'))
        userId=format(request.session.get('USER_ID'))
        wlCount=WishList.objects.filter(user=userId).count()
    page='Products'
    sub_page='Upload Mobile Photo'
    pgTitle=title+' | '+page
    record=Mobile.objects.get(id=pk)
    form=MobileTitlePhotoForm(instance=record)
    if request.method == 'POST':
        form=MobileTitlePhotoForm(request.POST,request.FILES,instance=record)
        if form.is_valid():
            form.save()
            messages.success(request, "Mobile Title Image Updated.")
            return redirect('products')
        else:
            print(form.errors)

    context={'form':form, 'page':page,'sub_page':sub_page,'pgTitle':pgTitle,'userType':userType,'loginId':loginId,'wlCount':wlCount}
    return render(request,'ShowRoom/mobile-photo-form.html',context)

def addMobilePhoto(request,pk):
    userType="Guest"
    loginId="Guest"
    userId=0
    wlCount=0
    if request.session.get('USER_LOGIN_ID') is not None:
        userType=format(request.session.get('USER_TYPE'))
        loginId=format(request.session.get('USER_LOGIN_ID'))
        userId=format(request.session.get('USER_ID'))
        wlCount=WishList.objects.filter(user=userId).count()
    page='Products'
    sub_page='Add Mobile Photo'
    pgTitle=title+' | '+page
    record=Mobile.objects.get(id=pk)
    rec=MobilePhoto()
    rec.mobile=record
    form=MobilePhotoForm(instance=rec)
    if request.method == 'POST':
        form=MobilePhotoForm(request.POST,request.FILES,instance=rec)
        if form.is_valid():
            form.save()
            messages.success(request, "Mobile Image Added.")
            return redirect('product',pk=pk)
        else:
            print(form.errors)

    context={'form':form, 'page':page,'sub_page':sub_page,'pgTitle':pgTitle,'userType':userType,'loginId':loginId,'wlCount':wlCount}
    return render(request,'ShowRoom/add-photo-form.html',context)

def product(request,pk):
    userType="Guest"
    loginId="Guest"
    userId=0
    wlCount=0
    if request.session.get('USER_LOGIN_ID') is not None:
        userType=format(request.session.get('USER_TYPE'))
        loginId=format(request.session.get('USER_LOGIN_ID'))
        userId=format(request.session.get('USER_ID'))
        wlCount=WishList.objects.filter(user=userId).count()
    page='Products'
    sub_page='Product'
    reviews=[]
    photos=[]
    record=Mobile.objects.get(id=pk)
    if record:
       sub_page=record.model
       photos=MobilePhoto.objects.filter(mobile=record)
       reviews=Comment.objects.filter(mobile=record);
    pgTitle=title+' | '+page
    context={'record':record,'photos':photos,'reviews':reviews,'page':page,'sub_page':sub_page,'pgTitle':pgTitle,'userType':userType,'loginId':loginId,'wlCount':wlCount}
    return render(request,'ShowRoom/product.html',context)

def brands(request):
    userType="Guest"
    loginId="Guest"
    userId=0
    wlCount=0
    if request.session.get('USER_LOGIN_ID') is not None:
        userType=format(request.session.get('USER_TYPE'))
        loginId=format(request.session.get('USER_LOGIN_ID'))
        userId=format(request.session.get('USER_ID'))
        wlCount=WishList.objects.filter(user=userId).count()
    page='Brands'
    sub_page='Brands'
    pgTitle=title+' | '+page
    records=Brand.objects.all()
    context={'records':records,'page':page,'sub_page':sub_page,'pgTitle':pgTitle,'userType':userType,'loginId':loginId,'wlCount':wlCount}
    return render(request,'ShowRoom/brands.html',context)

def addBrand(request):
    userType="Guest"
    loginId="Guest"
    userId=0
    wlCount=0
    if request.session.get('USER_LOGIN_ID') is not None:
        userType=format(request.session.get('USER_TYPE'))
        loginId=format(request.session.get('USER_LOGIN_ID'))
        userId=format(request.session.get('USER_ID'))
        wlCount=WishList.objects.filter(user=userId).count()
    page='Brands'
    sub_page='Add Brand'
    pgTitle=title+' | '+page
    form=BrandForm()
    if request.method == 'POST':
        form=BrandForm(request.POST)
        if form.is_valid():            
            form.save()
            messages.success(request, "Brand Record Added.")
            return redirect('brands')
        else:
            messages.error(request, "Some unknown error")

    context={'form':form,'page':page,'sub_page':sub_page,'pgTitle':pgTitle,'userType':userType,'loginId':loginId,'wlCount':wlCount}
    return render(request,'ShowRoom/brand-form.html',context)

def updateBrand(request,pk):
    userType="Guest"
    loginId="Guest"
    userId=0
    wlCount=0
    if request.session.get('USER_LOGIN_ID') is not None:
        userType=format(request.session.get('USER_TYPE'))
        loginId=format(request.session.get('USER_LOGIN_ID'))
        userId=format(request.session.get('USER_ID'))
        wlCount=WishList.objects.filter(user=userId).count()
    page='Brands'
    sub_page='Update Brand'
    pgTitle=title+' | '+page
    brand=Brand.objects.get(id=pk)
    form=BrandForm(instance=brand)
    if request.method == 'POST':
        form=BrandForm(request.POST,instance=brand)
        if form.is_valid():
            rec=Brand.objects.filter(Q(name=request.POST.get('name')) & ~Q(id=pk))
            if rec:
                messages.error(request, "Brand Name Alraedy exists.")              
            else:
                form.save()
                messages.success(request, "Brand details updated.")
                return redirect('brands')
        else:
            messages.error(request, "Some unknown error")

    context={'form':form, 'page':page,'sub_page':sub_page,'pgTitle':pgTitle,'userType':userType,'loginId':loginId,'wlCount':wlCount}
    return render(request,'ShowRoom/brand-form.html',context)

def uploadBrandPhoto(request,pk):
    userType="Guest"
    loginId="Guest"
    userId=0
    wlCount=0
    if request.session.get('USER_LOGIN_ID') is not None:
        userType=format(request.session.get('USER_TYPE'))
        loginId=format(request.session.get('USER_LOGIN_ID'))
        userId=format(request.session.get('USER_ID'))
        wlCount=WishList.objects.filter(user=userId).count()
    page='Brands'
    sub_page='Upload Brand Photo'
    pgTitle=title+' | '+page
    record=Brand.objects.get(id=pk)
    form=BrandTitlePhotoForm(instance=record)
    if request.method == 'POST':
        form=BrandTitlePhotoForm(request.POST,request.FILES,instance=record)
        if form.is_valid():
            form.save()
            messages.success(request, "Brand Title Image Updated.")
            return redirect('brands')
        else:
            print(form.errors)

    context={'form':form, 'page':page,'sub_page':sub_page,'pgTitle':pgTitle,'userType':userType,'loginId':loginId,'wlCount':wlCount}
    return render(request,'ShowRoom/brand-photo-form.html',context)

def register(request):
    userType="Guest"
    loginId="Guest"
    userId=0
    wlCount=0
    if request.session.get('USER_LOGIN_ID') is not None:
        userType=format(request.session.get('USER_TYPE'))
        loginId=format(request.session.get('USER_LOGIN_ID'))
        userId=format(request.session.get('USER_ID'))
        wlCount=WishList.objects.filter(user=userId).count()
    page='Register'
    sub_page='Register'
    pgTitle=title+' | '+page
    form=UserForm()
    if request.method == 'POST':
        form=UserForm(request.POST)
        if form.is_valid():
            rec=User.objects.filter(Q(name=request.POST.get('loginId')))
            if rec:
                messages.error(request, "Login ID Alraedy exists.")              
            else:
                form.save()
                messages.success(request, "User registration is successfull.")
                return redirect('login')
        else:
            messages.error(request, "Some unknown error")
    context={'form':form,'page':page,'sub_page':sub_page,'pgTitle':pgTitle,'userType':userType,'loginId':loginId,'wlCount':wlCount}
    return render(request,'ShowRoom/register.html',context)

def login(request):
    userType="Guest"
    loginId="Guest"
    userId=0
    wlCount=0
    if request.session.get('USER_LOGIN_ID') is not None:
        userType=format(request.session.get('USER_TYPE'))
        loginId=format(request.session.get('USER_LOGIN_ID'))
        userId=format(request.session.get('USER_ID'))
        wlCount=WishList.objects.filter(user=userId).count()
    page='Login'
    sub_page='Login'
    pgTitle=title+' | '+page
    if(request.method=="POST"):
        user=User.objects.filter(Q(loginId=request.POST.get('loginId')) & Q(password=request.POST.get('password')))
        if user:
            request.session['USER_ID'] = user[0].id
            request.session['USER_LOGIN_ID'] = user[0].loginId
            request.session['USER_NAME'] = user[0].name
            request.session['USER_TYPE'] = user[0].userType
            messages.success(request, "Logged in Successfully")
            return redirect('home')
        else:
            messages.error(request, "In-valid Login ID / Password")
    context={'page':page,'sub_page':sub_page,'pgTitle':pgTitle,'userType':userType,'loginId':loginId,'wlCount':wlCount}
    return render(request,'ShowRoom/login.html',context)


def addReview(request):
    userType="Guest"
    loginId="Guest"
    userId=0
    wlCount=0
    if request.session.get('USER_LOGIN_ID') is not None:
        userType=format(request.session.get('USER_TYPE'))
        loginId=format(request.session.get('USER_LOGIN_ID'))
        userId=format(request.session.get('USER_ID'))
        wlCount=WishList.objects.filter(user=userId).count()
    else:
        messages.error(request, "Please login to add a review")
        return redirect(request.META['HTTP_REFERER'])

    page='Login'
    sub_page='Login'
    pgTitle=title+' | '+page
    if(request.method=="POST"):
        prodId=request.POST.get('prodId')
        m=Mobile.objects.get(pk=prodId)
        u=User.objects.get(pk=userId)
        msg=request.POST.get('msg')
        c=Comment()
        c.user=u
        c.mobile=m
        c.msg=msg
        c.save()
        messages.success(request, "Review added Successfully")
        return redirect(request.META['HTTP_REFERER'])

    return redirect('home')

def logout(request):
    request.session.pop("USER_ID", None)
    request.session.pop("USER_LOGIN_ID", None)
    request.session.pop("USER_NAME", None)
    request.session.pop("USER_TYPE", None)
    messages.success(request, "Logged out Successfully")
    return redirect('home')

