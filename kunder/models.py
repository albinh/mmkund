"""Models for the mmkunder app"""
import uuid
from datetime import date
from math import floor


from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin


from django.db import models
from django.core.validators import RegexValidator




# Create your models here.
class Customer(models.Model):
    """
    Represents a customer and is "profile class" to the User class.
    """

    zip_validator = RegexValidator(r'^[0-9]{5}$', 'Bara siffror, utan mellanslag')
    phone_validator = RegexValidator(r'^07[0-9]{5,10}$', 'bara siffror i telefonnumret')

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    street = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=5, validators=[zip_validator])
    city = models.CharField(max_length=20)
    phone = models.CharField(max_length=20, validators=[phone_validator])
    active = models.BooleanField(default=True)
    user = models.OneToOneField("User", on_delete=models.CASCADE)
    week_0 = models.BooleanField(default=False)
    week_1 = models.BooleanField(default=False)
    email = models.EmailField(
        verbose_name='e-post',
        max_length=255,
        unique=True
    ) 

    def save(self, *args, **kwargs):
        if not hasattr(self, 'user'):
            self.user = User( is_active=True, is_superuser=False, is_staff=False )
            self.user.save()
        super().save(*args, **kwargs)  # Call the "real" save() method.


    def full_adress(self):
        return '%s %s %s' % (self.street, self.postal_code, self.city)

    cancels = models.ManyToManyField(
        "Delivery", related_name="canceled_customers", blank=True)

    def is_canceled(self, delivery):
        """ Check if this customer has canceled a specific delivery """
        return self.cancels.filter(pk=delivery.pk).count() > 0

    def cancel(self, delivery):
        """ cancel a specific delivevery """
        self.cancels.add(delivery)

    def uncancel(self, delivery):
        """ uncancel a previously canceled delivery """
        self.cancels.remove(delivery)

    def full_name(self):
        """ customer full name (first name + last name) """
        return '%s %s' % (self.first_name, self.last_name)

    def upcomming_deliveries_including_canceled(self):
        query = Delivery.objects.filter (  )



        if not self.week_0:
            query = query.exclude(week_0=True)
        if not self.week_1:
            query = query.exclude(week_1=True)
        return query

    def upcomming_deliveries(self):    
        return  self.upcomming_deliveries_including_canceled().exclude(canceled_customers=self)
        

class UserManager(BaseUserManager):
    """ ModelManager for User model """
  

    def create_superuser(self, email, password, username):
        """ Create superuser / staff """

        user = self.model(
            email=email,
            is_active=True,
            is_customer=False,
            is_superuser=True,
            is_staff=True,
            username=username
        )

        user.set_password(password)
        user.save()
        return user


class CustomerUserManager(UserManager):
    """ Manager for Customer """
    def get_queryset(self):
        """ return all users that is customers """
        return super().get_queryset().filter(is_customer=True)


class User(AbstractBaseUser, PermissionsMixin):
    REQUIRED_FIELDS=["email"]

    """ Customer User class. Either a staff or customer """
    email = models.EmailField(
        verbose_name='e-post',
        max_length=255,
        unique=False,
        blank=True
    )
    objects = UserManager()
    customers = CustomerUserManager()
    username = models.CharField(max_length=40, unique=True, default=uuid.uuid4)
    is_active = models.BooleanField(default=True)
    is_customer = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    USERNAME_FIELD = "username"


class DeliveryReciver(models.Model):
    """
    A reciver of a specific delivery
    When a delivery is populated the customers are "locked" as deliveryrecivers
    The customers adress is also saved to have a record of
    what was at the point of populate/delivery
    """
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    delivery = models.ForeignKey(
        "Delivery", on_delete=models.CASCADE, related_name='receiver')

    street = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=5, validators=[Customer.zip_validator])
    city = models.CharField(max_length=20)
    

class Delivery(models.Model):
    """ Model for a specific Delivery (past, current or future) """
    date = models.DateField()
    week_number = models.PositiveIntegerField()
    is_populated = models.BooleanField(default=False)
    week_0 = models.BooleanField(default=False)
    week_1 = models.BooleanField(default=True)
    def save(self, *args, **kwargs):
        self.week_0 = self.week_number()%2==0
        self.week_1 = self.week_number()%2==1
        super(Delivery, self).save(*args, **kwargs)


    def __str__ (self):
        return "%s #%s" % (self.date, self.week_number()) 

    def week_number(self):
        """
        return the week number.
        This is a custom numbering where 2018-01-01 is week 0.
        ISO week numbering is not used to make sure customer keeps getting every second week at
        the turn of the year.
        """
        # antal dagar sedan 1 januari 2018
        # Första veckan 2018 är vecka 0, per defintion

        days = (self.date - date(year=2018, month=1, day=1)).days

        return floor(days / 7)

    def is_week_1(self):
        """
        return true if week_number is in group 1
        """
        return self.week_number() % 2 == 1

    def is_week_0(self):
        """
        return true if week_number is in group 0
        """
        return self.week_number() % 2 == 0

    def forecast(self):
        """
        return a queryset representing the customers who will recive this delivery baesd
        on frequency, cancelations etc.

        Can not forecast already populated delivery
        """

        if self.is_populated:
            raise AttributeError(
                'Can not forecast an already populated delivery')

        if self.is_week_0():
            query = Customer.objects.filter(week_0=True)
        else:
            query = Customer.objects.filter(week_1=True)
        query = query.exclude(cancels__pk=self.pk)

        return query

    def populate(self):
        ''' "låser" kunder som ingår i denna leverans '''

        if self.date < date.today():
            raise AttributeError(
                'Can not populate delivery in the past')

        if self.is_populated:
            raise AttributeError(
                'Can not populate an already populated delivery')

        for customer in self.forecast():
            delivery_reciver = DeliveryReciver(delivery=self, customer=customer)
            delivery_reciver.save()

        self.is_populated = True
        self.save()
