from .models import Customers,Profession,DataSheet,Document
from rest_framework import serializers
class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model   =  Profession
        fields=('description',)


class DatasheetSerializer(serializers.ModelSerializer):
    class Meta:
        model=DataSheet
        fields=(
            'description',
            'historical_data'
             )


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        read_only_field=['customer']
        model=Document
        fields=(
            'dtype',
            'doc_number',
            'customer'
        )


class CustomerSerializer(serializers.ModelSerializer):
    num_profession = serializers.SerializerMethodField()
    data_sheet = DatasheetSerializer()
    profession = ProfessionSerializer(many=True)
    class Meta:
        model = Customers
        fields = ('id','name','address','data_sheet','profession','active','statuc_active','num_profession')
    def get_num_profession(self,obj):
        return obj.num_profession()

    def create(self, validated_data):
        professions = validated_data['profession']
        del  validated_data['profession']

        data_sheet = validated_data['data_sheet']
        del validated_data['data_sheet']

        d_sheet = DataSheet.objects.create(**data_sheet)
        customer = Customers.objects.create(**validated_data)
        customer.data_sheet = d_sheet

        for profession in professions:
            prof = Profession.objects.create(**profession)
            customer.profession.add(prof)
        customer.save()
        return customer
