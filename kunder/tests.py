from django.test import TestCase
from django.core.exceptions import ValidationError
from kunder.models import Customer, User, Delivery
from datetime import date

# Create your tests here.


class UserTestCase (TestCase):
    def setUp(self):
        pass

    def test_create_superuser(self):
        u = User.objects.create_superuser(email="albin@albinholmgren.se",
                                          password="password",
                                          username="albin")
        self.assertFalse(u.is_customer)
        self.assertTrue(u.is_superuser)
        self.assertTrue(u.is_staff)
        def f(): return u.customer
        self.assertRaises(AttributeError, f)

    def test_fullname(self):
        u = User.objects.create_user(email="test@test.com",
                                     first_name="Albin",
                                     last_name="Holmgren",
                                     postal_code="92294",
                                     city="Tvärålund",
                                     phone="0730241790",
                                     week_0=True,
                                     week_1=True)
        self.assertEqual(u.customer.full_name(), "Albin Holmgren")

    def test_create_customer(self):
        u = User.objects.create_user(email="test@test.com",
                                     first_name="Albin",
                                     last_name="Holmgren",
                                     postal_code="92294",
                                     city="Tvärålund",
                                     phone="0730241790",
                                     week_0=True,
                                     week_1=True,)
        self.assertEqual(u.email, "test@test.com")

        self.assertEqual(u.customer.first_name, "Albin")
        self.assertEqual(u.customer.last_name, "Holmgren")
        self.assertEqual(u.customer.postal_code, "92294")
        self.assertEqual(u.customer.city, "Tvärålund")
        self.assertEqual(u.customer.phone, "0730241790")
        self.assertEqual(u.customer.week_0, True)
        self.assertEqual(u.customer.week_1, True)

    def create_user ( self, id, week_0, week_1 ):
        return Customer( email="test@test.com",
                                      first_name="id",
                                      last_name="Holmgren",
                                      postal_code="92294",
                                      city="Tvärålund",
                                      phone="0730241790",
                                      week_0=week_0,
                                      week_1=week_1)

    def test_upcomming(self):
        c1 = self.create_user("alla", True, True)
        c2 = self.create_user("vecka0", True,False)
        c3 = self.create_user("vecka1", False, True)

        d1 = Delivery(date=date(year=2020, month=1, day=1))
        d1.save()
        d2 = Delivery(date=date(year=2020, month=1, day=8))
        d2.save()
        d3 = Delivery(date=date(year=2020, month=1, day=15))
        d3.save()
        d4 = Delivery(date=date(year=2020, month=1, day=22))
        d4.save()
        d5 = Delivery(date=date(year=2020, month=1, day=29))
        d5.save()

        c1.cancel(d1)
        c2.cancel(d1)
        c2.cancel(d2)
        self.assertEqual(c1.upcomming_deliveries().count(), 4 )
        self.assertEqual(c2.upcomming_deliveries().count(), 2 )
        self.assertEqual(c3.upcomming_deliveries().count(), 2 )


    def test_customers_manager(self):
        u = User.objects.create_superuser(email="albin@albinholmgren.se",
                                          password="password",
                                          username="albin")

        u2 = User.objects.create_user(email="test@test.com",
                                      first_name="Albin",
                                      last_name="Holmgren",
                                      postal_code="92294",
                                      city="Tvärålund",
                                      phone="0730241790",
                                      week_0=True,
                                      week_1=True,
                                      )

        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(User.customers.count(), 1)


class DeliveryTestCase(TestCase):
    def test_create_delivery(self):
        d = Delivery(date=date.today())
        self.assertEqual(d.date, date.today())

    def test_weeknumber(self):
        self.assertEqual(Delivery(date=date(2018, 1, 1)).week_number(), 0)
        self.assertEqual(Delivery(date=date(2018, 1, 8)).week_number(), 1)
        self.assertEqual(Delivery(date=date(2018, 1, 15)).week_number(), 0)
        
    def test_cancel(self):
        c1 = User.objects.create_user(email="test@test.com",
                                      first_name="all",
                                      last_name="Holmgren",
                                      postal_code="92294",
                                      city="Tvärålund",
                                      phone="0730241790",
                                      week_0=True,
                                      week_1=True,
                                      )
        c1.save()
        d = Delivery(date=date(year=2020, month=1, day=1))
        d.save()
        
        self.assertFalse(c1.customer.is_canceled(d))
        c1.customer.cancel(d)
        self.assertTrue(c1.customer.is_canceled(d))
        c1.customer.uncancel(d)
        self.assertFalse(c1.customer.is_canceled(d))
        

    def test_populate_old(self):
        d = Delivery(date=date(2019, 1, 17))
        # should not allow population of old deliveries
        self.assertRaises(AttributeError, d.populate)

    def test_cancel_populate(self):
        c1 = User.objects.create_user(email="test@test.com",
                                      first_name="all",
                                      last_name="Holmgren",
                                      postal_code="92294",
                                      city="Tvärålund",
                                      phone="0730241790",
                                      week_0=True,
                                      week_1=True,
                                      )
        c1.save()
        c2 = User.objects.create_user(email="test2@test.com",
                                      first_name="all2",
                                      last_name="Holmgren",
                                      postal_code="92294",
                                      city="Tvärålund",
                                      phone="0730241790",
                                      week_0=True,
                                      week_1=True
                                      )
        c2.save()
        d = Delivery(date=date(2030,1,1))
        d.save()
        c1.customer.cancel(d)

        d.populate()
        self.assertEqual(d.receiver.all().count(), 1)
        self.assertEqual(d.receiver.filter(customer__first_name="all2").count(), 1)


    def test_populate(self):
        c1 = User.objects.create_user(email="test@test.com",
                                      first_name="all",
                                      last_name="Holmgren",
                                      postal_code="92294",
                                      city="Tvärålund",
                                      phone="0730241790",
                                      week_0=True,
                                      week_1=True,
                                      )
        c1.save()
        c2 = User.objects.create_user(email="test2@test.com",
                                      first_name="week_0",
                                      last_name="Holmgren",
                                      postal_code="92294",
                                      city="Tvärålund",
                                      phone="0730241790",
                                      week_0=True,
                                      week_1=False
                                      )
        c2.save()
        c3 = User.objects.create_user(email="test3@test.com",
                                      first_name="week_1",
                                      last_name="Holmgren",
                                      postal_code="92294",
                                      city="Tvärålund",
                                      phone="0730241790",
                                      week_0=False,
                                      week_1=True
                                      )
        c3.save()

        week_0_delivery = Delivery(date=date(year=2024, month=1, day=8))
        week_0_delivery.save()
        week_0_delivery.populate()

        self.assertEqual(week_0_delivery.receiver.filter(customer__first_name="week_0").count(), 1)
        self.assertEqual(week_0_delivery.receiver.filter(customer__first_name="all").count(), 1)
        self.assertEqual(week_0_delivery.receiver.filter(customer__first_name="week_1").count(), 0)

        week_1_delivery = Delivery(date=date(year=2024, month=1, day=15))
        week_1_delivery.save()
        week_1_delivery.populate()
        self.assertEqual(week_1_delivery.receiver.filter(customer__first_name="week_0").count(), 0)
        self.assertEqual(week_1_delivery.receiver.filter(customer__first_name="all").count(), 1)
        self.assertEqual(week_1_delivery.receiver.filter(customer__first_name="week_1").count(), 1)

    def test_forecast(self):
        d = Delivery(date=date(2019, 1, 17))
        d.forecast()

    def test_double_populate(self):
        d = Delivery(date=date(year=2025, month=1, day=1))
        d.populate()
        self.assertRaises(AttributeError, d.populate)
