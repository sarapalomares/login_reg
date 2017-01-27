from __future__ import unicode_literals
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
import bcrypt, re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')




class UserManager(models.Manager):
    def validateReg(self, request):
        error = self.validate_inputs(request)
        print error

        if len(error) > 0:
            return(False, error)

        pw_hash = bcrypt.hashpw(request.POST['password_create'].encode(), bcrypt.gensalt())

        user = self.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email= request.POST['email'], pw_hash=pw_hash)

        return(True, user)



    def validate_inputs(self, request):
        error=[]
        if not request.POST['first_name'].isalpha() or not request.POST['last_name'].isalpha():
            error.append("The first or last name can't have numbers")
        if len(request.POST['first_name'])<2 or len(request.POST['last_name'])<2:
            error.append("Please input valid names")
        if not EMAIL_REGEX.match(request.POST['email']):
            error.append("Please input a valid email")
        if len(request.POST['password_create'])<8 or request.POST['password_create'] != request.POST['pw_confirm']:
            error.append("Passwords must match and be at least 8 characters.")
        # if len(request.POST['dob'])<8:
        #     error.append("Date of Birth should be in xx/xx/xxxx format")
        return error

    def validateLogin(self, request):
        try:
            user = User.objects.get(email=request.POST['user_email'])
            password = request.POST['password'].encode()
            if bcrypt.hashpw(password, user.pw_hash.encode()):
                return (True, user)

        except ObjectDoesNotExist:
            return(False, ["Email/password don't match."])

    # def contribute(self, form_data, user_id):
    #     try:
    #         quote = self.get_quote(form_data)
    #         user = User.objects.get(id=user_id)
    #         new_quote = Quote.objects.create(content=form_data['content'], user=user, quote=quote)
    #         return (True, new_quote)
    #     except:
    #         return (False, ["There was a problem contributing your quote..."])
    #
    # def get_quote(self, form_data):
    #     try:
    #         quote = Quote.objects.get(id=form_data['quote_id'])
    #     except:
    #         user = self.get_user(form_data)
    #         quote = Quote.objects.create(description=form_data['new_quote'], user=user)
    #     return quote
    #
    # def get_user(self, form_data):
    #     try:
    #         user = User.objects.get(id=form_data['user_id'])
    #     except:
    #         user = User.objects.create(name=form_data['new_user'])
    #     return user

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=100)
    pw_hash= models.CharField(max_length=300)
    # dob = models.DateField(auto_now=False, auto_now_add=False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

# class Quotes(models.Model) :
#     description = models.CharField(max_length=1000)
#     user = models.ForeignKey('User')
#     created_at = models.DateTimeField(auto_now_add = True)
#     updated_at = models.DateTimeField(auto_now = True)
#     objects = UserManager()
#
# class Favorites(models.Model):
#     user = models.ForeignKey('login_reg_app.User')
#     quote = models.ForeignKey('Quotes')
#     created_at = models.DateTimeField(auto_now_add = True)
#     updated_at = models.DateTimeField(auto_now = True)
#     objects = UserManager()
