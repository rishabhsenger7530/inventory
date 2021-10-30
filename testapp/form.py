from django import forms
from .models import User
from django.forms import ModelForm, widgets


from django.contrib.auth.forms import UserCreationForm

# Sign Up Form
class Usersignupform(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional',widget=forms.TextInput(attrs={'class':'form-control form-control-lg','placeholder':"Enter First Name", 'autocomplete':'off'}))
    last_name  = forms.CharField(max_length=30, required=False, help_text='Optional',widget=forms.TextInput(attrs={'class':'form-control form-control-lg','placeholder':"Enter Last Name", 'autocomplete':'off'}))
    email      = forms.EmailField(max_length=254, help_text='Enter a valid email address' ,widget=forms.TextInput(attrs={'class':'form-control form-control-lg','placeholder':"Enter Your Email", 'autocomplete':'off'}))
    contact    = forms.CharField(max_length=10, help_text='Enter a valid contact ',widget=forms.TextInput(attrs={'class':'form-control form-control-lg','placeholder':"Enter Contact", 'autocomplete':'off'}))
    # password1    = forms.CharField(max_length=10, help_text='Enter  valid Password ',widget=forms.PasswordInput(attrs={'class':'form-control form-control-lg','placeholder':"*****", 'autocomplete':'off'}))
    # password2    = forms.CharField(max_length=10, help_text='Enter  valid Confirm Password ',widget=forms.PasswordInput(attrs={'class':'form-control form-control-lg','placeholder':"*****", 'autocomplete':'off'}))
    class Meta:
        model = User
        fields = [
            'username', 
            'first_name', 
            'last_name', 
            'email', 
            'contact',
            'password1', 
            'password2', 
            ]
        widgets ={
                'username' : forms.TextInput(attrs={'class':'form-control form-control-lg','placeholder':"Enter User Name", 'autocomplete':'off'}),
                #'password1': forms.PasswordInput(attrs={'class':'form-control form-control-lg','placeholder':"********", 'autocomplete':'off'}),
                
        }



















# class Usersignupform(ModelForm):
#     email     = forms.EmailField(required=True,widget=forms.EmailInput(attrs={'class':'form-control form-control-lg','placeholder':"Enter Email", 'autocomplete':'off'}))
#     #contact   = forms.CharField(required=True,widget=forms.TextInput(attrs={'class':'form-control form-control-lg','placeholder':"Enter Contact", 'autocomplete':'off'}))
#     #username  = forms.CharField(required=True,widget=forms.TextInput(attrs={'class':'form-control form-control-lg','placeholder':"Enter Username", 'autocomplete':'off'}))
#     password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control form-control-lg','placeholder':"Enter Password", 'autocomplete':'off'}))
#     password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class':'form-control form-control-lg','placeholder':"Confirm Password", 'autocomplete':'off'}))
    
#     class Meta:
#         model = User
#         fields = ["first_name","last_name","email","username","contact","password1", "password2"]
#         widgets ={
#             'first_name': forms.TextInput(attrs={'class':'form-control form-control-lg','placeholder':"Enter First Name", 'autocomplete':'off'}),
#             'last_name': forms.TextInput(attrs={'class':'form-control form-control-lg','placeholder':"Enter Last Name", 'autocomplete':'off'}),
#             'username': forms.TextInput(attrs={'class':'form-control form-control-lg','placeholder':"Enter User Name", 'autocomplete':'off'}),
#             'contact': forms.TextInput(attrs={'class':'form-control form-control-lg','placeholder':"Enter Contact", 'autocomplete':'off'}),
            
#         }
    
#     def clean(self):
 
#         # data from the form is fetched using super function
#         super(Usersignupform, self).clean()
         
#         # extract the username and text field from the data
#         first_name    = self.cleaned_data.get('first_name')
#         last_name     = self.cleaned_data.get('last_name')
#         contact       = self.cleaned_data.get('contact')
#         username       = self.cleaned_data.get('username')
#         email         = self.cleaned_data.get('email')
#         password1     = self.cleaned_data.get('password1')
#         password2     = self.cleaned_data.get('password2')

 
#         # conditions to be met for the username length
#         if len(first_name) < 5:
#             self._errors['first_name'] = self.error_class([
#                 'Minimum 5 characters required'])
#         if len(last_name) <5:
#             self._errors['last_name'] = self.error_class([
#                 'Minimum 5 characters required'])
        
#         # if len(contact)!=10:
#         #     self._errors['contact'] = self.error_class([
#         #         'Minimum 10 characters required'])
#         # if len(email) < 10:
#         #     self._errors['email'] = self.error_class([
#         #         'Minimum 10 characters required'])
        
#         # if len(username) < 5:
#         #     self._errors['username'] = self.error_class([
#         #         'Minimum 5 characters required'])
        
#         # if password1!=password2:
#         #     self._errors['password1'] = self.error_class([
#         #         'Password Does not match'])
 
#         # return any errors if found
#         return self.cleaned_data
