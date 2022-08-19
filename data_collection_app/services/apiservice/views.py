from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
# from matplotlib.pyplot import get
from rest_framework import viewsets
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from apiservice.fetchObjList import *
from apiservice.models import Images,Annotations
from apiservice.serializers import ImageSerializer,AnnotationsSerialzier, ConsentSerializer
from datetime import datetime


class ApiViewSet(viewsets.ViewSet):
# Create your views here.
    @csrf_exempt
    def getImage(self, request, id=0):
        if request.method =='GET':

            images = Images.objects.exclude(
                Id__in=Annotations.objects.values_list('ImageId', flat=True)
                ).filter(Status=0).order_by('?').values('Id')[0:1].get()
            Images.objects.filter(Id=images['Id']).update(Status=1, DateFetched=datetime.now())
            img = Images.objects.all().filter(Id=images['Id'])
            image_serializer = ImageSerializer(instance=img, many=True)
         
            return JsonResponse(image_serializer.data, safe=False)
    
    
    @csrf_exempt
    def submitconsent(self, request):
        if request.method == 'POST':
            object = JSONParser().parse(request)
            # {'worker_id': 0, 'consent': False}
            print(object)
            consent_serializer = ConsentSerializer(data = {'WorkerId':object['worker_id'], 'Consent':object['consent']})
            if consent_serializer.is_valid():
                consent_serializer.save()
                return JsonResponse("Success",safe=False)
            else:
                print(consent_serializer.errors)
                return JsonResponse("Fail",safe=False)


            
            # print(object)
        


    @csrf_exempt
    def getObject(self, request, query):
        if request.method =='GET':
            # print(request.GET.get('word'))
            temp = esearch(query)
            print(query)
            # print(request)
            return JsonResponse(temp, safe=False)

    @csrf_exempt
    def saveAnnoatations(self, request):
        if request.method == 'POST':
            objects = JSONParser().parse(request)
            # print(objects['objects'][1])
            temp =[]
            for obj in objects['objects']:
                # print(obj)
                annotation_serializer = None
                data = {}
                data['WorkerId'] = obj['worker_id']
                data['ImageId'] = obj['image_id']
                data['ObjectName'] = obj['obj']
                data['Color'] = obj['color']
                data['Shape'] = obj['shape']
                data['PartObject'] = obj['obj_part']
                temp.append(data)
            
            if len(temp)!=0:
                print(temp)
                annotation_serializer = AnnotationsSerialzier(data = temp, many=True)
                if annotation_serializer.is_valid():
                    annotation_serializer.save()
                    return JsonResponse("Added" , safe=False)
                else:
                    print(annotation_serializer.errors)
                    return JsonResponse("Fail",safe=False)
            else:
                return JsonResponse("Fail",safe=False)
