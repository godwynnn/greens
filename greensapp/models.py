from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from django.contrib.auth.models import User

import datetime
from .formatchecker import ContentTypeRestrictedFileField


class Security(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING,blank=True,null= True,)
    secret_question = models.CharField(max_length=225,blank=True,default='')
    secret_answer = models.CharField(max_length=225,blank=True,default='')
    previous_email = models.CharField(max_length=225,blank=True,default='')
    last_token = models.CharField(max_length=225,blank=True,default='')
    profile_updated = models.BooleanField(default=False,blank=True)
    suspension_count = models.IntegerField(default=0,blank=True)
    briefly_suspended = models.BooleanField(default=False,blank=True)
    time_suspended = models.DateTimeField(null=True, blank=True)
    time_suspended_timestamp = models.IntegerField(default=0,blank=True)
    locked = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=45, blank=True, default ='')
    email_confirmed = models.BooleanField(default=False)
    two_factor_auth_enabled = models.BooleanField(default=False)
    email_change_request = models.BooleanField(default=False)
    pending_email = models.EmailField(default='',blank=True)
    login_attempt_count = models.IntegerField(default=0)
    class Meta:
        db_table = 'security'


    def save(self,*args, **kwargs):

        if self.suspension_count>2:
            self.briefly_suspended = True
            self.time_suspended =  datetime.datetime.now()
            self.time_suspended_timestamp = datetime.datetime.now().timestamp()
        secret_question=''
        for char in self.secret_question:
            if char ==  '?':
                continue
            else:
                secret_question = secret_question +char
        self.secret_question = secret_question+'?'
        super(Security,self).save()



class Userprofile(models.Model):
    user=models.OneToOneField(User,null=True,blank=True,on_delete=models.CASCADE)
    image=models.ImageField(upload_to='profile_pic/', null=True,blank=True, default='user.png')

    class Meta:
        ordering=['-id']
        db_table='profiles'

    def __str__(self):
        return f"{self.user} - Profile"

    
        



class Tag(models.Model):
    name=models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    title=models.CharField(max_length= 200)
    image=models.ImageField(upload_to='image', blank=True,null=True)
    slug=models.SlugField(unique=True,null=True,blank=True)
    content=models.TextField(blank=True,null=True)
    tags=models.ManyToManyField(Tag)
    price=models.PositiveIntegerField(blank=True,null=True,default=0)
    date_added=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now= True)

    class Meta:
        ordering=['-date_added']

    def save(self, *args,**kwargs):
        if self.slug == None:
            slug=slugify(self.title)
            has_slug=Product.objects.filter(slug=slug)
            count =1
            while has_slug:
                count +=1
                slug=slugify(self.title) + '-' + str(count)
                has_slug=Product.objects.filter(slug=slug).exists()

            self.slug=slug
        super().save(*args,**kwargs)

    def __str__(self):
        return self.title


class Orderitem(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    item=models.ForeignKey(Product,on_delete=models.CASCADE,null=True,blank=True)
    member_id=models.CharField(max_length=1000, null=True,blank=True)
    ordered = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"orders-{self.item.title}- {self.quantity}"

    def product_price(self):
        return self.quantity*self.item.price



ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)


class Address(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,null=True,blank=True)
    street_address = models.TextField(max_length=100)
    country = models.CharField(max_length=50)
    member_id=models.CharField(max_length=1000, null=True,blank=True)
    zip = models.CharField(max_length=100)
    address_type = models.CharField(max_length=1000, choices=ADDRESS_CHOICES,default='B')
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Addresses'

class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    addr=models.ForeignKey(Address,blank=True,null=True,on_delete=models.CASCADE)
    items=models.ManyToManyField(Orderitem)
    member_id=models.CharField(max_length=1000, null=True,blank=True)
    ordered_date = models.DateTimeField(auto_now_add=True)
    ordered = models.BooleanField(default=False)

    def __str__(self):
    
        return self.member_id

    def summed_product_price(self):
        for product in self.items.all():
            return product.product_price()
        
    def total_price(self):
        total=0
        for product in self.items.all():
            total += product.product_price()
        return total

    def total_count(self):
        return self.items.count()





class QuerySearch(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    query=models.CharField(max_length=500)
    date_searched=models.DateTimeField(auto_now_add=True)


class PostType(models.Model):
    type=models.CharField(max_length=20,null=True,blank=True)

    def __str__(self):
        return self.type

class Social(models.Model):
    user=models.ForeignKey(User,null=True,blank=True,on_delete=models.CASCADE)
    title=models.CharField(max_length=1000,null=True,blank=True)
    content=models.TextField(max_length=1000000,null=True,blank=True)
    file = ContentTypeRestrictedFileField(upload_to='media/',blank=True, null=True)
    likes=models.ManyToManyField(User,blank=True, related_name='likers',default=0)
    # like_count=models.PositiveBigIntegerField(null=True,blank=True)
    category=models.CharField(max_length=1000,null=True,blank=True)
    lat=models.CharField(max_length=500,null=True,blank=True)
    long=models.CharField(max_length=500,null=True,blank=True)
    address=models.CharField(null=True,blank=True,max_length=1000)
    date_added=models.DateTimeField(auto_now=True)
    date_update=models.DateTimeField(auto_now_add=True),

    class Meta:
        db_table='Socials'

    def __str__(self):
        return f"{self.user.username}: {self.title}"

    # def save(self,*args,**kwargs):
    #     self.like_count=int(self.likes.all().count())

    #     super(Social,self).save(*args,**kwargs)

class Comment(models.Model):
    user=models.ForeignKey(User,null=True,blank=True,on_delete=models.CASCADE)
    post=models.ForeignKey(Social,related_name='comments',null=True,blank=True,on_delete=models.CASCADE)
    content=models.TextField(max_length=10000,null=True,blank=True)
    is_reply = models.BooleanField(default=0)
    message_replied= models.IntegerField(blank=True,null=True)
    
    def __str__(self):
        return f"{self.user.username}: {self.post.title}"


# class Maps(models.Model):
#     user=models.ForeignKey(User,null=True,blank=True,on_delete=models.CASCADE)
#     lat=models.IntegerField(default=0,null=True,blank=True)
#     long=models.IntegerField(default=0,null=True,blank=True)
#     address=models.CharField(null=True,blank=True,max_length=1000)
#     def __str__(self):
#         return f"{self.user.username}: {self.lat}-{self.long}"