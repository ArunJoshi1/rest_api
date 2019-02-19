from django.shortcuts import render
from .models import Customers,Profession,DataSheet,Document
from rest_framework import viewsets
from rest_framework.filters import SearchFilter,OrderingFilter
from .serializers import CustomerSerializer,ProfessionSerializer,DatasheetSerializer,DocumentSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import (AllowAny,
                                        IsAdminUser,
                                        IsAuthenticatedOrReadOnly,
                                        DjangoModelPermissions,
                                        DjangoModelPermissionsOrAnonReadOnly
                                        )
# Create your views here.



class Customer(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    filter_backends = (DjangoFilterBackend,SearchFilter,OrderingFilter)
    filter_fields = ('name',)
    search_fields = ('name', 'address')
    ordering_fields=("name", "id",'address')
    ordering = ('name',)
    lookup_field = 'name'
    authentication_classes = [TokenAuthentication,]
    def get_queryset(self):
        status = True if self.request.query_params.get('active') == 'False' else True
        address = self.request.GET.get('address',None)
        if address:
            customer = Customers.objects.filter(address__icontains=address,active=status)
        else:
            customer = Customers.objects.filter(active=status)
        return customer
    
    
    # def list(self, request, *args, **kwargs):
    #     customer=self.get_queryset()
    #     serializer=CustomerSerializer(customer,many=True)
    #     return Response(serializer.data)

    # def create(self, request, *args, **kwargs):
    #     data = request.data
    #     customer = Customers.objects.create(
    #         name=data['name'],
    #         address=data['address'],
    #         data_sheet_id=data['data_sheet'],
    #     )
    #     profession= Profession.objects.get(id=data['profession'])
    #     customer.profession.add(profession)
    #     customer.save()
    #     serializer = CustomerSerializer(customer)
    #     return  Response(serializer.data)

    def update(self, request, *args, **kwargs):
        customer = self.get_object()
        data=request.data
        customer.name = data['name']
        customer.address = data['address']
        customer.data_sheet_id = data['data_sheet']
        profession = customer.profession.all()
        for p in profession:
            customer.profession.remove(p)

        profession = Profession.objects.get(id=data['profession'])
        customer.profession.add(profession)
        customer.save()
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        customer = self.get_object()
        customer.name = request.data.get('name',customer.name)
        print(customer.name)
        customer.data_sheet_id = request.data.get('data_sheet',customer.data_sheet_id)
        customer.address = request.data.get('address',customer.address)
        customer.save()
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        customer = self.get_object()
        customer.delete()
        return Response("object removed")


    @action(detail=True)
    def deactivate(self, request,**kwargs):
        customer = self.get_object()
        customer.active = False

        customer.save()
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)
    @action(detail=False)
    def deactivate_All(self,request,**kwargs):
        customer = Customers.objects.all()
        customer.update(active=False)

        serializer = CustomerSerializer(customer, many=True)
        return Response(serializer.data)

    @action(detail=False)
    def activate_All(self, request, **kwargs):
        customer = Customers.objects.all()
        customer.update(active=True)

        serializer = CustomerSerializer(customer, many=True)
        return Response(serializer.data)

    @action(detail=False,methods=['POST'])
    def change_status(self,request,**kwargs):
        status=request.data['active']
        customer = self.get_queryset()
        customer.update(active=status)
        serializer = CustomerSerializer(customer, many=True)
        return Response(serializer.data)
    
    
    
    
class Professionviewset(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    authentication_classes = [TokenAuthentication, ]
    queryset =  Profession.objects.all()
    serializer_class = ProfessionSerializer
class Datasheetviewset(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)

    queryset = DataSheet.objects.all()
    serializer_class = DatasheetSerializer

class Document(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer