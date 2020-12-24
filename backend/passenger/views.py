from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions
from functools import partial
from .models import Passenger
from .serializers import PassengerRegistrationSerializer
from .serializers import PassengerLoginSerializer
from .serializers import GetAvailableCabSerializer, BookCabSerializer



class CustomPermissionsForPassenger(permissions.BasePermission):

    def __init__(self, allowed_methods):
        self.allowed_methods = allowed_methods

    def has_permission(self, request, view):
        if 'passenger_id' in request.session.keys():
            return request.method in self.allowed_methods

class PassengerRegistration(APIView):
    """
   View for passenger registration

    """
    serializer_class = PassengerRegistrationSerializer

    def get(self, request, format=None):
        customers = Passenger.objects.all()
        serializer = PassengerRegistrationSerializer(customers, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = PassengerRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PassengerLogin(APIView):
    """ View for passenger login """

    serializer_class = PassengerLoginSerializer

    def post(self, request, format=None):
        serializer = PassengerLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            request.session['passenger_id'] = serializer.validated_data["passenger_id"]
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookCab(APIView):

    """
     View for booking cab

    """
    serializer_class = BookCabSerializer
    permission_classes = (partial(CustomPermissionsForPassenger, ['GET', 'HEAD', 'POST']),)

    def post(self, request, format=None):
        context = {
            'passenger_id': request.session['passenger_id'],
            'source_address': request.session['source_address'],
            'destination_address': request.session['destination_address']
            }
        serializer = BookCabSerializer(data=request.data, context=context)
        if serializer.is_valid():
            serializer.save()
            data = {
                "Success": "Cab booked successfully"
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class Logout(APIView):
    """ View for passenger account logout"""

    def get(self, request, format=None):
        del request.session['passenger_id']
        data = {'Logout': 'logged out successfully'}
        return Response(data, status=status.HTTP_200_OK)
