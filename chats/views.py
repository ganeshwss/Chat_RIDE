from django.shortcuts import render
from .serializers import *
from .models import *
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import status
from django.http import JsonResponse
import base64
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated

#view messages api - for particular room
class ViewMessages(generics.GenericAPIView):
    serializer_class = ViewMessageSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, room_name):
        try:
            item = ChatModel.objects.filter(room_name=room_name)
            serializer = ViewMessageSerializer(item, many=True)
            return JsonResponse({"status": "success", "message": serializer.data}, safe=False, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# To convert Image into BS64 format
@api_view(['POST'])
def uploadImage(request):
    try:
        file = request.FILES.get('file')
        b64_string = base64.b64encode(file.read())
        return JsonResponse({"status": "success", "BS64_Image": b64_string.decode("utf-8")}, status=status.HTTP_200_OK)
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

#  To get all room list exists in the Chat App Database
class ViewRoomList(generics.GenericAPIView):
    serializer_class = ViewMessageSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request , platform_name):
        try:
            room_list = []
            plt = ChatModel.objects.filter(platform_name = platform_name)
            
            for p in plt:
                if p.room_name not in room_list:
                    room_list.append(p.room_name)

            print(room_list)
            return JsonResponse({"status": "success", "message": room_list, "no_of_rooms": len(room_list)}, safe=False, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
