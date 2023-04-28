from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics

from api.serializers import *
from api.models import *


class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        print(request.data)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class EventAPIListView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = Events.objects.all()
    serializer_class = EventSerializer


class EventRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = Events.objects.all()
    serializer_class = EventSerializer


class CategoryAPIListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryItemsAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, pk):
        events = Events.objects.filter(category_id=pk)
        serializer = EventSerializer(instance=events, many=True)
        return Response(serializer.data)


class FavoritesAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        liked_events = Events.objects.filter(user=request.user.id, liked_events__user_liked=True)
        print(request.user)
        serializer = EventSerializer(instance=liked_events, many=True)
        return Response(serializer.data)


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
