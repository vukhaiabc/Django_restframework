from django.urls import path,re_path,include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('courses',views.CourseViewSet,'courses')
router.register('lesson',views.LessonViewSet,'lessons')
router.register('user',views.UserViewSet,'user')
router.register('category',views.CategoryViewSet,'category')
router.register('comment',views.CommentViewSet,'comment')

app_name = 'courses_app'
urlpatterns = [
    path('',include(router.urls)),
]