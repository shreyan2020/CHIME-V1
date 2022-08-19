from rest_framework import serializers
from apiservice.models import Annotations, Images, Consent


class ConsentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consent
        fields =('Id', 'WorkerId', 'Consent', 'DateSubmitted')

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields =('Id', 'ImageName','Status', 'ModelName')

class AnnotationsSerialzier(serializers.ModelSerializer):
    # def to_internal_value(self, data):
    #     if data.get('ParentObject', None) == '':
    #         data.pop('ParentObject')
    #     return super(AnnotationsSerialzier, self).to_internal_value(data)
    class Meta:
        model = Annotations
        fields = ('Id','ImageId','ObjectName','PartObject','Color','Shape','WorkerId','DateSubmitted')
        