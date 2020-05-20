"""Park Areas for Kennywood Amusement Park"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from kennywoodapi.models import ParkArea


class ParkAreaSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ParkArea
        url = serializers.HyperlinkedIdentityField(
            view_name='parkarea',
            lookup_field='id'
        )
        fields = ('id', 'url', 'name', 'theme')


class ParkAreas(ViewSet):
    def create(self, request):
        newarea = ParkArea()
        newarea.name = request.data["name"]
        newarea.theme = request.data["theme"]
        newarea.save()
        serializer = ParkAreaSerializer(newarea, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            area = ParkArea.objects.get(pk=pk)
            serializer = ParkAreaSerializer(area, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        area = ParkArea.objects.get(pk=pk)
        area.name = request.data["name"]
        area.theme = request.data["theme"]
        area.save()
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        try:
            area = ParkArea.objects.get(pk=pk)
            area.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except ParkArea.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        areas = ParkArea.objects.all()
        serializer = ParkAreaSerializer(
            areas, many=True, context={'request': request})
        return Response(serializer.data)
