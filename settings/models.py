from django.db import models
from django.utils.translation import gettext as _
from django_countries.fields import CountryField

# Create your models here.
class Company(models.Model):
    name = models.CharField(max_length=100 , verbose_name =_("Name")) 
    logo = models.ImageField(_("Logo"), null= True , blank = True ,upload_to = 'settings/company')
    desc = models.TextField(_("Description"), null=True , blank=True, max_length= 500  )
    call_us = models.CharField(_("Call_Us"), max_length=25)
    email_us = models.EmailField(_("Email_Us"), max_length=254)
    fb_link = models.URLField(_("Facebook"), max_length=200 ,null=True ,blank=True)
    insta_link = models.URLField(_("Instagram"), max_length=200 ,null=True ,blank=True)
    linkedin_link = models.URLField(_("Linkedin"), max_length=200 ,null=True ,blank=True)
    twit_link = models.URLField(_("Twitter"), max_length=200 ,null=True ,blank=True)
    emails = models.TextField(_("Emails") , max_length=100 ,null=True ,blank=True)
    numbers = models.TextField(_("Numbers"), max_length=100 ,null=True ,blank=True)
    country = CountryField(blank= True)
    address = models.TextField(_("Address") , max_length=100 ,null=True ,blank=True)


    def __str__(self) :
        return self.name