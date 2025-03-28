from . import views
from django.urls import path


app_name = "pages"


urlpatterns = [
    path('solutions/', views.ArticleList.as_view(), name='article-list'),
    path('solutions/<slug:slug>/', views.ArticleDetail.as_view(), name='article-detail'),
    
]
