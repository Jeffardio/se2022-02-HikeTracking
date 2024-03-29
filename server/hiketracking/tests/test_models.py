# Create your tests here.
from django.contrib.auth import get_user_model, authenticate
from django.test import Client
from django.test import TestCase

from hiketracking.models import Hike, Point, Hut, ParkingLot, Facility, HutFacility, CustomerProfile, CustomUser, HutWorker, HutHike
from hiketracking.tests.test_utilty import CreateTestUser
from hiketracking.views.view_hike import Recommended


class UsersManagersTests(TestCase):

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            email='mona131376st@gmail.com', password='foo', role="hi")
        self.assertEqual(user.email, 'mona131376st@gmail.com')
        self.assertFalse(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(user.username)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email='')
        with self.assertRaises(ValueError):
            User.objects.create_user(email='', password="foo", role="hi")

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            email='super@user.com', role="hi", password='foo')
        self.assertEqual(admin_user.email, 'super@user.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(admin_user.username)
        except AttributeError:
            pass
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email='super@user.com', password='foo', role="hi", is_superuser=False)

    def util(self):
        User = get_user_model()
        user = User.objects.create_user(
            email='normal@user.com', password='johnpassword', role='hi')
        self.assertEqual(user.email, 'normal@user.com')
        self.assertFalse(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        user.is_active = True

    # try to log in and the check result of login
    # password is incorrect and login failed
    # current information and login success
    # because of this project uses django default login, it tests django api using in fact

    def test_login(self):
        self.util()
        c = Client()
        response = c.post('/login/', {'username': 'john', 'password': 'smith'})
        self.assertEqual(response.status_code, 404)

    # try to log out and the check result of logout
    def test_logout(self):
        self.util()
        c = Client()
        response = c.post(
            '/login/', {'username': 'normal@user.com', 'password': 'johnpassword'})
        self.assertEqual(response.status_code, 404)
        response = c.get('/customer/details/')
        response = c.logout()
        self.assertIsNone(response, "NoneType")


class LoginTest(TestCase):

    def setUp(self):
        User = get_user_model()
        user = User.objects.create_user(
            email='test@user.com', password='foo', role='smth', is_active=1)
        self.assertEqual(user.email, 'test@user.com')
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_confirmed)
        user.is_active = True

    def test_credentials(self):
        user = authenticate(email='test@user.com', password='foo')
        self.assertTrue((user is not None) and user.is_authenticated)

    def test_invalid_email(self):
        user = authenticate(email='invlaid', password='foo')
        self.assertFalse(user is not None and user.is_authenticated)

    def test_invalid_password(self):
        user = authenticate(email='test@user.com', password='doo')
        self.assertFalse(user is not None and user.is_authenticated)

    def test_user_is_active(self):
        user = authenticate(email='test@user.com', password='foo')
        self.assertEqual(user.is_active, True)

    def test_user_is_not_confirmed(self):
        user = authenticate(email='test@user.com', password='foo')
        self.assertEqual(user.is_confirmed, False)


def setup_utils_hike():
    User = get_user_model()
    User.objects.create_user(email='test@user.com',
                             password='foo', role='smth')
    user_id = User.objects.get(email='test@user.com')
    p1 = Point(latitude=0.01, longitude=0.01, province="test province", village="test village",
               address="test address")
    p1.save()
    Hike.objects.create(title='Climbing', length=2, expected_time=1, ascent=1, difficulty='easy', start_point=p1,
                        end_point=p1, local_guide=user_id)
    Hike.objects.create(title='Trekking', length=3, expected_time=2, ascent=0, difficulty='medium', start_point=p1,
                        end_point=p1, local_guide=user_id)


class FullListHikeTest(TestCase):

    def setUp(self):
        setup_utils_hike()

    # Test to get full list of hikes

    def test_get_full_list_of_hikes(self):
        hike_list = Hike.objects.all()
        self.assertEqual(len(hike_list), 2)
        h_list = list(hike_list.values())
        val_list = list(h_list[0].values())
        val_list_1 = list(h_list[1].values())
        final_test_list = [val_list, val_list_1]
        self.assertEqual(final_test_list[0][1], 'Climbing')
        self.assertEqual(final_test_list[1][8], 1)


class AddHikeDescriptionTest(TestCase):
    def setUp(self):
        setup_utils_hike()

    def test_add_hike_description(self):
        hike_concerned = Hike.objects.get(id=1)
        self.assertEqual(hike_concerned.description, '')
        Hike.objects.filter(id=1).update(description='A beginner Hike')
        hike_updated = Hike.objects.get(id=1)
        self.assertEqual(hike_updated.description, 'A beginner Hike')


class listParkingPotTest(TestCase):
    def setUp(self):
        User = get_user_model()
        User.objects.create_user(
            email='test@user.com', password='foo', role='smth')
        user_id = User.objects.get(email='test@user.com')
        p1 = Point(latitude=0.01, longitude=0.01, province="test province", village="test village",
                   address="test address")
        park1 = ParkingLot(name="test parking pot name 1",
                           fee=0.01, n_cars=1, point_id=1)
        p1.save()
        park1.Point = p1
        park1.save()
        return super().setUp()

    def testListParkingPot(self):
        list = ParkingLot.objects.all()
        self.assertEqual(list[0].fee, 0.01)
        self.assertEqual(list[0].name, "test parking pot name 1")
        self.assertEqual(list[0].n_cars, 1)
        self.assertEqual(list[0].point_id, 1)


class AddHutTest(TestCase):
    def setUp(self):
        User = get_user_model()
        User.objects.create_user(
            email='test@user.com', password='foo', role='smth')
        self.user_id = User.objects.get(email='test@user.com')

        return super().setUp()

    def testHut(self):
        p1 = Point(latitude=0.01, longitude=10.01, province="test province", village="test village",
                   address="test address")
        p1.save()

        hunt = Hut(name="test parking pot name 1", n_beds=2,
                   fee=10.01, ascent=10,
                   phone="+999222", email="md@gmail.com",
                   web_site="www.hi.com",
                   desc="testHunt", point_id=1)
        hunt.Point = p1
        hunt.save()
        service = ["serve1", "serve2"]

        hut_list = Hut.objects.all()
        self.assertEqual(hut_list[0].fee, 10.01)
        self.modelvalues(hunt, hut_list, service)

    def modelvalues(self, hunt, hut_list, service):
        self.assertEqual(hut_list[0].name, "test parking pot name 1")
        self.assertEqual(hut_list[0].n_beds, 2)
        self.assertEqual(hut_list[0].point_id, 1)
        for service_ in service:
            obj, isNew = Facility.objects.get_or_create(name=service_)
            self.assertTrue(isNew)
            HutFacility.objects.get_or_create(hut=hunt, facility=obj)
        services = Facility.objects.all()
        self.assertEqual(len(services), 2)
        self.assertEqual(len(HutFacility.objects.filter(hut=hunt).all()), 2)

    def testHutTextFee(self):
        p1 = Point(latitude=0.01, longitude=10.01, province="test province", village="test village",
                   address="")
        hunt = Hut(name="test parking pot name 1", n_beds=2,
                   fee=10, ascent=10,
                   phone="+999222", email="md@gmail.com",
                   web_site="www.hi.com",
                   desc="testHunt", point_id=1)
        service = ["serve1", "serve2"]
        p1.save()
        hunt.Point = p1
        hunt.save()

        list = Hut.objects.all()
        self.assertEqual(list[0].fee, 10)
        self.modelvalues(hunt, list, service)


class AddParkingLotTest(TestCase):

    def setUp(self):
        User = get_user_model()
        User.objects.create_user(
            email='test@user.com', password='foo', role='smth')
        User.objects.get(email='test@user.com')
        Point.objects.create(latitude=0.01, longitude=0.01, province="start province", village="start village",
                             address="start address")
        ParkingLot.objects.create(
            name="test parking lot name 2", fee=0.05, n_cars=5, point_id=1)

    def test_add_parking_lot(self):
        park = ParkingLot.objects.all()
        self.assertEqual(park[0].fee, 0.05)
        self.assertEqual(park[0].name, "test parking lot name 2")
        self.assertEqual(park[0].n_cars, 5)


class RetrieveHutTest(TestCase):

    def setUp(self):
        p1 = CreateTestUser()
        Hut.objects.create(name="TestHut", n_beds=1, fee=20, point_id=p1.id)

    def test_retrieve_hut(self):
        concerned_hut = Hut.objects.get(name="TestHut")
        self.assertEqual(concerned_hut.n_beds, 1)
        self.assertEqual(concerned_hut.fee, 20)
        self.assertEqual(concerned_hut.desc, " ")
        self.assertEqual(concerned_hut.point_id, 1)


def setup_reccom_util():
    User = get_user_model()
    User.objects.create_user(
        email='test@user.com', password='foo', role='smth')
    user_id = User.objects.get(email='test@user.com')
    p1 = Point(latitude=0.01, longitude=0.01, province="test province",
                village="test village", address="test address")
    p1.save()
    Hike.objects.create(title='Climbing', length=2, expected_time=1, ascent=1,
                        difficulty='easy', start_point=p1, end_point=p1, local_guide=user_id)
    Hike.objects.create(title='Trekking', length=3, expected_time=2, ascent=0,
                        difficulty='medium', start_point=p1, end_point=p1, local_guide=user_id)
    

class recommendedHikeTest(TestCase):
    def setUp(self) -> None:
        setup_reccom_util()
        return super().setUp()

    def test_recommendHike(self):

        pass


class modifyAndDeleteHikeTest(TestCase):
    def setUp(self) -> None:
        setup_reccom_util()
        return super().setUp()

    def assert_util(self, hike1):
        self.assertEqual(hike1[1].title, "Trekking")
        self.assertEqual(hike1[1].length, 3)
        self.assertEqual(hike1[1].expected_time, 2)
        self.assertEqual(hike1[1].ascent, 0)
        self.assertEqual(hike1[1].difficulty, 'medium')
        self.assertEqual(hike1[1].start_point.latitude, 0.01)
        self.assertEqual(hike1[1].start_point.longitude, 0.01)
        self.assertEqual(hike1[1].start_point.province, "test province")
        self.assertEqual(hike1[1].start_point.village, "test village")
        self.assertEqual(hike1[1].start_point.address, "test address")
        self.assertEqual(hike1[0].end_point.latitude, 0.01)
        self.assertEqual(hike1[0].end_point.longitude, 0.01)
        self.assertEqual(hike1[0].end_point.province, "test province")
        self.assertEqual(hike1[0].end_point.village, "test village")
        self.assertEqual(hike1[0].end_point.address, "test address")

    def test_context(self):
        hike1 = Hike.objects.all()
        self.assertEqual(hike1[0].title, "Climbing")
        self.assertEqual(hike1[0].length, 2)
        self.assertEqual(hike1[0].expected_time, 1)
        self.assertEqual(hike1[0].ascent, 1)
        self.assertEqual(hike1[0].difficulty, 'easy')
        self.assertEqual(hike1[0].start_point.latitude, 0.01)
        self.assertEqual(hike1[0].start_point.longitude, 0.01)
        self.assertEqual(hike1[0].start_point.province, "test province")
        self.assertEqual(hike1[0].start_point.village, "test village")
        self.assertEqual(hike1[0].start_point.address, "test address")
        self.assertEqual(hike1[0].end_point.latitude, 0.01)
        self.assertEqual(hike1[0].end_point.longitude, 0.01)
        self.assertEqual(hike1[0].end_point.province, "test province")
        self.assertEqual(hike1[0].end_point.village, "test village")
        self.assertEqual(hike1[0].end_point.address, "test address")

        self.assert_util(hike1)

    def test_modifyHike(self):
        hike1 = Hike.objects.get(title="Climbing")
        hike1.title = "modifyTest"
        hike1.length = 10
        hike1.expected_time = 10
        hike1.ascent = 10
        hike1.difficulty = "hard"
        hike1.start_point.latitude = 0.1
        hike1.start_point.province = "modifyTestProvince"
        hike1.start_point.village = "modifyTestVillage"
        hike1.start_point.address = "modifyTestAddress"
        hike1.end_point.latitude = 0.1
        hike1.end_point.province = "modifyTestProvince"
        hike1.end_point.village = "modifyTestVillage"
        hike1.end_point.address = "modifyTestAddress"
        hike1.save()
        hike1 = Hike.objects.all()
        self.assertEqual(hike1[0].title, "modifyTest")
        self.assertEqual(hike1[0].length, 10)
        self.assertEqual(hike1[0].expected_time, 10)
        self.assertEqual(hike1[0].ascent, 10)
        self.assertEqual(hike1[0].difficulty, 'hard')
        self.assertEqual(hike1[0].start_point.latitude, 0.01)
        self.assertEqual(hike1[0].start_point.longitude, 0.01)
        self.assertEqual(hike1[0].start_point.province, "test province")
        self.assertEqual(hike1[0].start_point.village, "test village")
        self.assertEqual(hike1[0].start_point.address, "test address")
        self.assertEqual(hike1[0].end_point.latitude, 0.01)
        self.assertEqual(hike1[0].end_point.longitude, 0.01)
        self.assertEqual(hike1[0].end_point.province, "test province")
        self.assertEqual(hike1[0].end_point.village, "test village")
        self.assertEqual(hike1[0].end_point.address, "test address")

        self.assert_util(hike1)

    def test_deleteHikeById(self):
        obj = Hike.objects.get(title="Trekking")
        obj.delete()
        hike2 = Hike.objects.all()
        self.assertTrue(hike2.exists())

    def test_deleteAllHikes(self):
        Hike.objects.all().delete()
        hike2 = Hike.objects.all()
        self.assertFalse(hike2.exists())


class CustomerProfileTest(TestCase):
    def setUp(self) -> None:
        c1 = CustomUser(email="test@test.com", role="Testrole")
        c1.save()
        CustomerProfile.objects.create(
            user=c1, min_length=0.01, max_length=0.01, min_time=1, max_time=1, min_altitude=1, max_altitude=1)
        return super().setUp()

    def test_CustomerProfile(self):
        cp1 = CustomerProfile.objects.all()
        self.assertEqual(cp1[0].user.email, "test@test.com")
        self.assertEqual(cp1[0].user.role, "Testrole")
        self.assertEqual(cp1[0].min_length, 0.01)
        self.assertEqual(cp1[0].max_length, 0.01)
        self.assertEqual(cp1[0].min_time, 1)
        self.assertEqual(cp1[0].max_time, 1)
        self.assertEqual(cp1[0].min_altitude, 1)
        self.assertEqual(cp1[0].max_altitude, 1)


class HutWorkerTest(TestCase):

    def setUp(self):
        User = get_user_model()
        User.objects.create_user(
            email='test@user.com', password='foo', role='HutWorker')
        user_id = User.objects.get(email='test@user.com')
        p1 = Point(latitude=0.01, longitude=0.01, province="test province", village="test village",
                   address="test address")
        p1.save()
        testHike = Hike.objects.create(title='Climbing', length=2, expected_time=1, ascent=1, difficulty='easy', start_point=p1,
                                       end_point=p1, local_guide=user_id)
        testHut = Hut.objects.create(
            name="TestHut", n_beds=1, fee=20, point_id=p1.id)
        testHutHike = HutHike.objects.create(
            hike_id=testHike.id, hut_id=testHut.id)

        HutWorker.objects.create(hut_id=testHut.id, hutworker_id=user_id.id)

    def test_hutworker(self):

        h = HutWorker.objects.all()
        self.assertEqual(h[0].hut_id, 1)
        self.assertEqual(h[0].hutworker_id, 1)

    def test_hike_condition(self):
        h = HutWorker.objects.all()
        huthike = HutHike.objects.all()
        if h[0].hut_id == 1:
            if huthike[0].hike_id == 1:
                Hike.objects.filter(id=huthike[0].hike_id).update(
                    condition="Closed")

        hike = Hike.objects.all()
        self.assertEqual(hike[0].condition, "Closed")


class AccountConfirmationTest(TestCase):

    def setUp(self):

        c1 = CustomUser(email="test@atest.com",
                        role="local guide", is_staff=0, is_active=1)
        c1.save()

        c2 = CustomUser(email="test@test.com", role="Platform Manager",
                        is_staff=0, is_confirmed=1, is_active=1)
        c2.save()


    def assert_util(self,cust_upd) :
        self.assertEqual(cust_upd[0].email, "test@atest.com")
        self.assertEqual(cust_upd[0].role, "local guide")
        self.assertEqual(cust_upd[0].is_staff, 0)
        self.assertEqual(cust_upd[0].is_active, 1)


    def test_confirming_user(self):

        cust = CustomUser.objects.all()

        if cust[1].role == "Platform Manager":
            if cust[0].is_confirmed == 0:
                CustomUser.objects.filter(
                    role=cust[0].role).update(is_confirmed=1)

        cust_upd = CustomUser.objects.all()
        self.assert_util(cust_upd)
        self.assertEqual(cust_upd[0].is_confirmed, 1)

    def test_not_confirmed_user(self):
        cust_upd = CustomUser.objects.all()
        self.assert_util(cust_upd)
        self.assertEqual(cust_upd[0].is_confirmed, 0)
