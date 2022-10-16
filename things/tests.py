from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import Thing
# Create your tests here.
class ThingsTestCase(TestCase):
    def setUp(self):
        self.thing = Thing.objects.create(
            name="John",
            description = 'Hi. This is John',
            quantity=100
        )

    #~~~~~~~~~UNIT TESTS FOR NAME~~~~~~~~~~~~~~~~#
    
    def test_name_must_be_unique(self):
        second_thing = self._create_second_thing()
        self.thing.name = second_thing.name
        self._assert_user_is_invalid()

    def test_name_must_not_be_blank(self):
        self.thing = ''
        self._assert_user_is_invalid()
    
    def test_name_can_be_50_characters_long(self):
        self.thing.name =  'x' * 50
        self._assert_user_is_valid()   

    def test_name_cannot_be_over_50_characters_long(self):
        self.thing.name = 'x' * 51
        self._assert_user_is_invalid()


    #~~~~~~~~~UNIT TESTS FOR DESCRIPTION~~~~~~~~~~~~~~#
    
    def test_description_may_be_unique(self):
        second_thing = self._create_second_thing()
        self.thing.description = second_thing.description
        self._assert_user_is_valid()

    def test_description_may_be_blank(self):
        self.thing = ''
        self._assert_user_is_valid()
    
    def test_description_can_be_120_characters_long(self):
        self.thing.description =  'x' * 120
        self._assert_user_is_valid()   

    def test_description_cannot_be_over_120_characters_long(self):
        self.thing.description = 'x' * 121
        self._assert_user_is_invalid()


    #~~~~~~~~~UNIT TESTS FOR QUANTITY~~~~~~~~~~~~~~~~#
    
    def test_quantity_need_not_be_unique(self):
        second_thing = self._create_second_thing()
        self.thing.quantity = second_thing.quantity
        self._assert_user_is_valid()
        
    def test_quantity_can_be_0(self):
        self.thing.quantity = 0
        self._assert_user_is_valid()   

    def test_quantity_cannot_be_less_than_0(self):
        self.thing.quantity = -1
        self._assert_user_is_invalid()   

    def test_quantity_can_be_100(self):
        self.thing.quantity = 100
        self._assert_user_is_valid()   

    def test_name_cannot_be_greater_than_100(self):
        self.thing.quantity = 101
        self._assert_user_is_invalid()
    
    #~~~~~~~~~UNIT TESTS FOR QUANTITY~~~~~~~~~~~~~~~~#
    def _assert_user_is_valid(self):
        try:
            self.user.full_clean()
        except(ValidationError):
            self.fail('Test user should be valid')

    def _assert_user_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.user.full_clean()

    def _create_second_thing(self):
        thing = Thing.objects.create(
            name= "John",
            description = 'Hi. This is John.',
            quantity = 100,
        )
        return thing