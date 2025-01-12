from django.db import models
from datetime import date
from django.db.models import F
from decimal import *
from django.utils.translation import gettext as _

# Create your models here.
CHOICE_ACTIVE="ACTIVE"
STATUS_CHOICES = [
    ("ACTIVE", "ACTIVE"),
    ("DISABLE", "DISABLE"),
]

CHOICE_STATUS="NEW"
MOBILE_STATUS_CHOICES = [
    ("NEW", "NEW"),
    ("OLD", "OLD"),
    ("DISCONTINUED", "DISCONTINUED"),
]

CHOICE_DIMENTION="mm"
DIMENTIONS_CHOICES = [
    ("mm", "mm"),
    ("cm", "cm")
]

CHOICE_MEMORY="GB"
MEMORY_CHOICES = [
    ("MB", "MB"),
    ("GB", "GB"),
    ("TB", "TB")
]

CHOICE_YES="YES"
YESNO_CHOICES = [
    ("YES", "YES"),
    ("NO", "NO"),
]

CHOICE_SIM="4G"
SIM_CHOICES = [
    ("GSM", "GSM"),
    ("3G", "3G"),
    ("4G", "4G"),
    ("5G", "5G"),
]

CHOICE_GENDER="FEMALE"
GENDER_CHOICES = [
        ("FEMALE", "FEMALE"),
        ("MALE", "MALE"),
]

CHOICE_USER="USER"
USER_CHOICES = [
    ("ADMIN", "ADMIN"),
    ("USER", "USER"),
]

class Brand(models.Model):
    name = models.CharField(max_length=200)
    photo = models.ImageField(null=True, default="image.png")
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default=CHOICE_ACTIVE)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['name']
    def __str__(self):
        return self.name
    

class Mobile(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    model = models.CharField(max_length=200)
    os = models.CharField(max_length=200)
    colors = models.CharField(max_length=200)    
    price = models.DecimalField(max_digits=8,decimal_places=1)
    weight = models.IntegerField(null=True,default=0)
    announcedDate = models.DateField(_("Date"), default=date.today)
    launchDate = models.DateField(_("Date"), default=date.today)
    screenWidth = models.DecimalField(max_digits=8,decimal_places=1)
    screenHeight = models.DecimalField(max_digits=8,decimal_places=1)
    width = models.DecimalField(max_digits=8,decimal_places=1)
    height = models.DecimalField(max_digits=8,decimal_places=1)
    length = models.DecimalField(max_digits=8,decimal_places=1)
    dimentionUnit = models.CharField(max_length=20,choices=DIMENTIONS_CHOICES,default=CHOICE_DIMENTION)
    ram = models.IntegerField(null=True,default=0)
    ramUnit = models.CharField(max_length=20,choices=MEMORY_CHOICES,default=CHOICE_MEMORY)
    rom = models.IntegerField(null=True,default=0)
    romUnit = models.CharField(max_length=20,choices=MEMORY_CHOICES,default=CHOICE_MEMORY)    
    bluetooth = models.CharField(max_length=200)
    btVersion=models.DecimalField(max_digits=8,decimal_places=1,default=0.0)
    wifi = models.CharField(max_length=200)
    wifiVersion=models.DecimalField(max_digits=8,decimal_places=1,default=0.0)
    frontCams= models.IntegerField(null=True,default=0)
    fCam1Res = models.DecimalField(max_digits=8,decimal_places=1,default=0.0)
    fCam2Res = models.DecimalField(max_digits=8,decimal_places=1,default=0.0)
    fCam3Res = models.DecimalField(max_digits=8,decimal_places=1,default=0.0)
    fCamFlash = models.CharField(max_length=20,choices=YESNO_CHOICES,default=CHOICE_YES)
    backCams= models.IntegerField(null=True,default=0)
    bCam1Res = models.DecimalField(max_digits=8,decimal_places=1,default=0.0)
    bCam2Res = models.DecimalField(max_digits=8,decimal_places=1,default=0.0)
    bCam3Res = models.DecimalField(max_digits=8,decimal_places=1,default=0.0)
    bCam4Res = models.DecimalField(max_digits=8,decimal_places=1,default=0.0)
    bCamFlash = models.CharField(max_length=20,choices=YESNO_CHOICES,default=CHOICE_YES)
    fm = models.CharField(max_length=20,choices=YESNO_CHOICES,default=CHOICE_YES)
    sims= models.IntegerField(null=True,default=1)
    sim1Network = models.CharField(max_length=10,choices=SIM_CHOICES,default=CHOICE_SIM)
    sim2Network = models.CharField(max_length=10,choices=SIM_CHOICES,default=CHOICE_SIM)
    sim3Network = models.CharField(max_length=10,choices=SIM_CHOICES,default=CHOICE_SIM)
    sim4Network = models.CharField(max_length=10,choices=SIM_CHOICES,default=CHOICE_SIM)
    battery = models.IntegerField(null=True,default=0)
    photo = models.ImageField(null=True, default="no-image.png")
    description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20,choices=MOBILE_STATUS_CHOICES,default=CHOICE_STATUS)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['announcedDate']
    def __str__(self):
        return self.name

class MobilePhoto(models.Model):
    mobile = models.ForeignKey(Mobile, on_delete=models.CASCADE)
    photo = models.ImageField(null=True, default="no-image.png")
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['-created','-updated']
    def __str__(self):
        return self.mobile.model

class User(models.Model):
    name = models.CharField(max_length=200)
    loginId = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    gender = models.CharField(max_length=20,choices=GENDER_CHOICES,default=CHOICE_GENDER)
    userType = models.CharField(max_length=20,choices=USER_CHOICES,default=CHOICE_USER)
    email = models.CharField(max_length=200)
    contact = models.CharField(max_length=20)
    address = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default=CHOICE_ACTIVE)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['name']
    def __str__(self):
        return self.name

class Comment(models.Model):
    mobile = models.ForeignKey(Mobile, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    msg = models.CharField(max_length=300)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['-created','-updated']
    def __str__(self):
        return self.name
    
class Rating(models.Model):
    mobile = models.ForeignKey(Mobile, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=8,decimal_places=1,default=0.0)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['-created','-updated']
    def __str__(self):
        return self.name
    
class WishList(models.Model):
    mobile = models.ForeignKey(Mobile, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['-created','-updated']
    def __str__(self):
        return self.mobile.model





# class Company(models.Model):
#     name = models.CharField(max_length=200)
#     photo = models.ImageField(null=True, default="image.png")
#     status = models.CharField(max_length=20,choices=STATUS_CHOICES,default=CHOICE_ACTIVE)
#     created=models.DateTimeField(auto_now_add=True)
#     updated=models.DateTimeField(auto_now=True)
#     class Meta:
#         ordering = ['name']
#     def __str__(self):
#         return self.name
    
# class Car(models.Model):
#     company = models.ForeignKey(Company, on_delete=models.CASCADE)
#     name = models.CharField(max_length=200)
#     color = models.CharField(max_length=200)
#     model = models.CharField(max_length=200)
#     year = models.CharField(max_length=20)
#     price = models.CharField(max_length=20)
#     engineType = models.CharField(max_length=20)
#     transmission = models.CharField(max_length=200)
#     status = models.CharField(max_length=20, default="ACTIVE")
#     created=models.DateTimeField(auto_now_add=True)
#     updated=models.DateTimeField(auto_now=True)
#     class Meta:
#         ordering = ['name']
#     def __str__(self):
#         return self.name
    
# class CarPhoto(models.Model):
#     car = models.ForeignKey(Car, on_delete=models.CASCADE)
#     photo = models.ImageField(null=True, default="image.png")
#     created=models.DateTimeField(auto_now_add=True)
#     updated=models.DateTimeField(auto_now=True)
#     class Meta:
#         ordering = ['-created','-updated']
#     def __str__(self):
#         return self.car.name
