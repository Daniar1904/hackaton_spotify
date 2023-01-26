from django.urls import path, include
from . import views
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
# router.register('sounds', views.SoundViewSet)

"""Прописываем пути нашим атрибутам(комментариям, лайкам, подпискам)"""

urlpatterns = [
    # path('', include(router.urls)),
    path('comments/', views.CommentCreateView.as_view()),
    path('comments/<int:pk>/', views.CommentDetailView.as_view()),
    path('likes/', views.LikeCreateView.as_view()),
    path('likes/<int:pk>/', views.LikeDeleteView.as_view()),
    path('followings-sounds/', views.FollowedUsersPostsView.as_view()),
]