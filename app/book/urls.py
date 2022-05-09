from book import views
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('genre', views.GenreViewSet)
router.register('author', views.AuthorViewSet)
router.register('publihouse', views.PublishingHouseViewSet)
router.register('book', views.BookViewSet)

app_name = 'book'

urlpatterns = [
    path('', include(router.urls))
]
