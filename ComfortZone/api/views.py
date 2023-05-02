from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics

from api.serializers import *
from api.models import *
from rest_framework.viewsets import ViewSet
class UserViewSet(ViewSet):
    def create_user(self, request, *args, **kwargs):
        serializer = CreateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.create_user(**serializer.validated_data)
        return Response(serializer.validated_data, status=status.HTTP_201_CREATED)

class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        print(request.data)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)





class EventAPIListView(APIView):
    permission_classes = (AllowAny,)
    def post(self, request, *args, **kwargs):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventRetrieveUpdateDestroyAPIView(APIView):
    permission_classes = (AllowAny,)
    def get_object(self, pk):
        try:
            return Events.objects.get(id=pk)
        except Events.DoesNotExist as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk):
        self.permission_classes = (AllowAny,)
        instance = self.get_object(pk)
        serializer = EventSerializer(instance)
        return Response(serializer.data)

    def put(self, request, pk, *args, **kwargs):
        self.permission_classes = (IsAuthenticated,)
        instance = self.get_object(pk)
        serializer = EventSerializer(instance=instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,pk):
        self.permission_classes = (IsAuthenticated,)
        instance = self.get_object(pk)
        serializer = EventSerializer(instance=instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class CategoryAPIListView(APIView):
    permission_classes = (AllowAny,)
    def get(self,request):
        queryset = Category.objects.all()
        serializer = CategorySerializer(queryset,many=True)
        return Response(serializer.data)

class CategoryItemsAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, pk):
        events = Events.objects.filter(category_id=pk)
        serializer = EventSerializer(instance=events, many=True)
        return Response(serializer.data)

class FavoritesAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        liked_events = LikeUser.objects.filter(user=request.data.user)


@api_view(['POST'])
def like(request, pk):
    try:
        event = Events.objects.get(pk=pk)
    except Exception as e:
        return Response({"message": f"{e}"})
    if LikeUser.objects.filter(user=request.user, event=event).exists():
        k = LikeUser.objects.get(user=request.user, event=event)
        if k.user_liked:
            k.user_liked = False
        else:
            k.user_liked = True
        k.save()
        return Response({"message0": "success"})
    likesave = LikeUser.objects.create(user=request.user, event=event, user_liked=True)
    likesave.save()
    return Response({"message": "success"})
