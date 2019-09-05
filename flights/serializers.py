from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Flight, Booking, Profile

from django.utils import timezone


class FlightSerializer(serializers.ModelSerializer):
	class Meta:
		model = Flight
		fields = ['destination', 'time', 'price', 'id']


class BookingSerializer(serializers.ModelSerializer):
	flight = serializers.SlugRelatedField(slug_field='destination',read_only=True)
	class Meta:
		model = Booking
		fields = ['flight', 'date', 'id']


class BookingDetailsSerializer(serializers.ModelSerializer):
	flight = FlightSerializer()
	total = serializers.SerializerMethodField()
	class Meta:
		model = Booking
		fields = ['flight', 'date', 'passengers', 'id','total']

	def get_total(self,obj):
		return obj.passengers * obj.flight.price





class AdminUpdateBookingSerializer(serializers.ModelSerializer):
	class Meta:
		model = Booking
		fields = ['date', 'passengers']


class UpdateBookingSerializer(serializers.ModelSerializer):
	class Meta:
		model = Booking
		fields = ['passengers']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name']

    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        new_user = User(username=username, first_name=first_name, last_name=last_name)
        new_user.set_password(password)
        new_user.save()
        return validated_data

class Userinfo(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['first_name', 'last_name']



class ProfileSerializer(serializers.ModelSerializer):
	user = Userinfo()
	past_bookings = serializers.SerializerMethodField()
	tier = serializers.SerializerMethodField()
	class Meta:
		model = Profile
		fields = ['user', 'miles','past_bookings','tier']


	def get_past_bookings(self,obj):
		bookings = obj.user.bookings.filter(date__lt=timezone.now())
		return BookingSerializer(bookings, many =True).data



	def get_tier(self,obj):
		if obj.miles >= 0 and obj.miles <=9999:
			tier = 'Blue'
		elif obj.miles >= 10000 and obj.miles <=59999:
			tier = 'Silver'
		elif obj.miles >= 60000 and obj.miles <= 99999:
			tier = 'Gold'
		else:
			tier = 'Platinum'

		return tier
















