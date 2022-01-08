from django.urls import path, include
from rest_framework.routers import DefaultRouter
from watchlist_app.api.views import (WatchlistAPIView, WatchlistDetailAPIView, StreamPlatformViewset, StreamPlatformAPIView, StreamPlatformDetailAPIView,
                                     ReviewList, ReviewDetail, ReviewCreate, UserReview, WatchlistGV)


router = DefaultRouter()
router.register('stream', StreamPlatformViewset, basename='streamplatformviewset')


urlpatterns = [
    path('list/', WatchlistAPIView.as_view(), name='WatchlistListAPIView'),
    path('list2/', WatchlistGV.as_view(), name='WatchlistGV'),
    path('<int:pk>', WatchlistDetailAPIView.as_view(), name='WatchlistDetailAPIView'),

    path('', include(router.urls)),
    # path('stream/', StreamPlatformAPIView.as_view(), name='StreamPlatformAPIView'),
    # path('stream/<int:pk>', StreamPlatformDetailAPIView.as_view(), name='StreamPlatformDetailAPIView'),

    # path('review/', ReviewList.as_view(), name='ReviewList'),
    # path('review/<int:pk>', ReviewDetail.as_view(), name='ReviewDetail'),

    path('<int:pk>/review-create', ReviewCreate.as_view(), name='ReviewCreate'),
    path('<int:pk>/reviews', ReviewList.as_view(), name='ReviewList'),
    path('review/<int:pk>', ReviewDetail.as_view(), name='ReviewDetail'),
    path('reviews', UserReview.as_view(), name='UserReview'),
    
]