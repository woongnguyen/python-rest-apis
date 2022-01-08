from rest_framework.views import APIView
from rest_framework import generics, mixins, pagination, viewsets
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import status
from django.shortcuts import get_object_or_404
from watchlist_app.models import Watchlist, StreamPlatform, Review
from watchlist_app.api.serializers import WatchlistSerializer, StreamPlatformSerializer, ReviewSerializer
from watchlist_app.api.permissions import IsAdminOrReadOnly, IsReviewUserOrReadOnly
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle, ScopedRateThrottle
from watchlist_app.api.throttling import ReviewCreateThrott, ReviewListThrott
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from watchlist_app.api.pagination import WatchlistPagination

class UserReview(generics.ListAPIView):
        # queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # permission_classes = [IsAuthenticated]
    # throttle_classes = [ReviewListThrott, AnonRateThrottle]

    # def get_queryset(self):
    #     username = self.kwargs.get('username')
    #     return Review.objects.filter(author__username=username)
    
    def get_queryset(self):
        username = self.request.query_params.get('username', None)
        return Review.objects.filter(author__username=username)


class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [ReviewCreateThrott]

    def get_queryset(self):
        return Review.objects.all()


    def perform_create(self, serializer):
        pk = self.kwargs['pk']
        watchlist = Watchlist.objects.get(pk=pk)

        author = self.request.user
        review_queryset = Review.objects.filter(watchlist=watchlist, author=author)

        if review_queryset.exists():
            raise ValidationError('You have already reviewed this movie')

        if watchlist.number_rating == 0:
            watchlist.avg_rating = serializer.validated_data['rating']
        else:
            watchlist.avg_rating = (watchlist.avg_rating + serializer.validated_data['rating']) /2
        
        watchlist.number_rating = watchlist.number_rating + 1
        watchlist.save()

        serializer.save(watchlist=watchlist, author=author)


class ReviewList(generics.ListAPIView):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # permission_classes = [IsAuthenticated]
    # throttle_classes = [ReviewListThrott, AnonRateThrottle]
    filter_backends = [DjangoFilterBackend,filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['author__username', 'active']
    search_fields = ['watchlist__title', 'author__username']
    ordering_fields = ['rating', 'author__username']


    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return Review.objects.filter(watchlist=pk)


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewUserOrReadOnly]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'ReviewDetail'


# class ReviewList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
    
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)


# class ReviewDetail(mixins.RetrieveModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

class StreamPlatformViewset(viewsets.ModelViewSet):
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer
    permission_classes = [IsAdminOrReadOnly]

# class StreamPlatformViewset(viewsets.ViewSet):

#     def list(self, request):
#         queryset = StreamPlatform.objects.all()
#         serializer = StreamPlatformSerializer(queryset, many=True)
#         return Response(serializer.data)
    
#     def retrieve(self, request, pk=None):
#         queryset = StreamPlatform.objects.all()
#         watchlist = get_object_or_404(queryset, pk=pk)
#         serializer = StreamPlatformSerializer(watchlist)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = StreamPlatformSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)



class StreamPlatformAPIView(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        queryset = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(queryset, many=True)
        return Response(serializer.data)


    def post(self, request):
        serializer = StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class StreamPlatformDetailAPIView(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request, pk, *args, **kwargs):
        try:
            queryset = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = StreamPlatformSerializer(queryset)
        return Response(serializer.data)


    def put(self, request, pk, *args, **kwargs):
        queryset = StreamPlatform.objects.get(pk=pk)
        serializer = StreamPlatformSerializer(queryset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk, *args, **kwargs):
        queryset = StreamPlatform.objects.get(pk=pk)
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class WatchlistGV(generics.ListAPIView):
    queryset = Watchlist.objects.all()
    serializer_class = WatchlistSerializer
    pagination_class = WatchlistPagination
    # permission_classes = [IsAuthenticated]
    # throttle_classes = [ReviewListThrott, AnonRateThrottle]
    filter_backends = [DjangoFilterBackend,filters.SearchFilter, filters.OrderingFilter]
    # filterset_fields = ['author__username', 'active']
    search_fields = ['platform__name']
    ordering_fields = ['number_rating', 'avg_rating']


class WatchlistAPIView(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request, *args, **kwargs):
        queryset = Watchlist.objects.all()
        serializer = WatchlistSerializer(queryset, many=True)
        return Response(serializer.data)


    def post(self, request, *args, **kwargs):
        serializer = WatchlistSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class WatchlistDetailAPIView(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request, pk, *args, **kwargs):
        try:
            queryset = Watchlist.objects.get(pk=pk)
        except Watchlist.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = WatchlistSerializer(queryset)
        return Response(serializer.data)


    def put(self, request, pk, *args, **kwargs):
        queryset = Watchlist.objects.get(pk=pk)
        serializer = WatchlistSerializer(queryset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk, *args, **kwargs):
        queryset = Watchlist.objects.get(pk=pk)
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)