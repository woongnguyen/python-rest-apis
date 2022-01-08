# from django.shortcuts import render
# from watchlist_app.models import Movie
# from django.http import JsonResponse
# # Create your views here.


# def MovieList(request):
#     movies = Movie.objects.all()
#     data = {'status': 200,
#             'result': list(movies.values())
#             }
#     return JsonResponse(data)


# def MovieDetail(request, pk):
#     movie = Movie.objects.get(pk=pk)
#     data = {'status': 200,
#             'result': {
#                 'name': movie.name,
#                 'remarks': movie.remarks,
#                 'active': movie.active,
#                 }
#             }
#     return JsonResponse(data)
