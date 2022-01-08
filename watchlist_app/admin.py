from django.contrib import admin
from watchlist_app.models import StreamPlatform, Watchlist, Review


# Register your models here.
admin.site.register(Watchlist)
admin.site.register(StreamPlatform)
admin.site.register(Review)
