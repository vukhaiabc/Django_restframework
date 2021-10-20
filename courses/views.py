from rest_framework import viewsets,permissions,generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from django.db.models import F
from rest_framework.parsers import MultiPartParser
from .models import Course,Lesson,User,Category,Tag,Action,Rating,LessonView,LessonComment
from .serializers import (
    CourseSerializer,
    TagSerializer,
    LessonSerializer,
    LessonDetailSerializer,
    UserSerializer,
    CategorySerializer,
    ActionSerializer,
    RatingSerializer,
    LessonViewSerializer,
    LessonCommentSerializer
)
from .paginator import BasePagination


# API rest_framework
class UserViewSet(viewsets.ViewSet,generics.ListAPIView, generics.CreateAPIView,generics.RetrieveAPIView):
    queryset = User.objects.filter(is_active = True)
    serializer_class = UserSerializer
    parser_classes = [MultiPartParser,]

    def get_permissions(self):
        if self.action == 'retrieve' :
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]
class CategoryViewSet(viewsets.ViewSet,generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
class CourseViewSet(viewsets.ViewSet,generics.ListAPIView,generics.CreateAPIView,generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CourseSerializer
    pagination_class = BasePagination

    def get_queryset(self):
        courses = Course.objects.filter(active=True)
        q = self.request.query_params.get('q')
        if q is not None:
            courses = courses.filter(name__icontains=q)
        cate_id = self.request.query_params.get('category_id')
        if cate_id is not None:
            courses = courses.filter(category__id = cate_id)

        return courses

    @action(['get'], detail=True, url_path='lessons')
    def get_lessons(self,request,pk):
        course = self.get_object()
        les = course.lessons.filter(active = True)

        key = self.request.query_params.get('key')
        if key is not None:
            les = les.filter(name__icontains = key)

        return Response(data=LessonSerializer(les,many=True).data,status=status.HTTP_200_OK)

    # permission_classes = [permissions.IsAuthenticated,]

    # def get_permissions(self):
    #     if self.action == 'list' :
    #         return [permissions.AllowAny()]
    #     return [permissions.IsAuthenticated()]

class LessonViewSet(viewsets.ViewSet,generics.RetrieveAPIView):
    queryset = Lesson.objects.filter(active = True)
    serializer_class = LessonDetailSerializer

    def get_permissions(self):
        if self.action in ['take_action','take_rating','add_comment'] :
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    @action(methods=['post'], detail=True, url_path='add-comment')
    def add_comment(self,request,pk):
        try:
            lesson = self.get_object()
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)
        content = request.data.get('content')
        if content :
            comment = LessonComment.objects.create(content = content,lesson= lesson, creator = request.user)
            return Response(data=LessonCommentSerializer(comment).data,status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


    @action(methods=['get'],detail=True,url_path='tags')
    def get_tag(self,request,pk):
        try:
            lesson = self.get_object()
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)
        tag = lesson.tag.all()
        return Response(data=TagSerializer(tag,many=True).data,status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True, url_path='addtags')
    def add_tag(self, request, pk):
        try:
            lesson = self.get_object()
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else :
            tags_res = request.data.get('tags')
            if tags_res is not None :
                for tag in tags_res:
                    t,_ = Tag.objects.get_or_create(name = tag)
                    lesson.tag.add(t)
                lesson.save()
                return Response(data=TagSerializer(lesson.tag.all(),many=True).data,status=status.HTTP_201_CREATED)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'],detail=True,url_path='like')
    def take_action(self,request,pk):
        try:
            lesson = self.get_object()
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            type_action = int(request.data.get('type'))
        except ValueError | IndexError :
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else :
            action = Action.objects.create(type=type_action,lesson=lesson,creator = request.user)
            return Response(data=ActionSerializer(action).data,status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True, url_path='rating')
    def take_rating(self, request, pk):
        try:
            lesson = self.get_object()
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            rate = int(request.data.get('rate'))
        except ValueError | IndexError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            r = Rating.objects.create(rate = rate, lesson=lesson,creator = request.user)
            return Response(data=RatingSerializer(r).data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True, url_path='views')
    def incre_view(self, request, pk):
        try:
            lesson = self.get_object()
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)
        lesson_view,_ = LessonView.objects.get_or_create(lesson = lesson)
        lesson_view.views = F('views')+1
        lesson_view.save()

        lesson_view.refresh_from_db()

        return Response(data=LessonViewSerializer(lesson_view).data,status=status.HTTP_200_OK)

    @action(methods=['get'],detail=True,url_path="hide-lesson",url_name="hide_lesson")
    def hide_lesson(self,request,pk):
        try:
            l = Lesson.objects.get(pk=pk)
            l.active = False
            l.save()
        except Lesson.DoesNotExist :
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(data=LessonSerializer(l,context={'request':request}).data,status=status.HTTP_200_OK)
    # list (get) : Xem danh sach khoa hoc
    # list (post) : them khoa hoc
    # detail : xem chi tiet 1 khoa hoc
    # put : cap nhat khoa hoc
    # delete : xoa khoa hoc
class CommentViewSet(viewsets.ViewSet,generics.DestroyAPIView,generics.UpdateAPIView):
    queryset = LessonComment.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LessonCommentSerializer

    def destroy(self,request, *args, **kwargs):
        if request.user == self.get_object().creator :
            return super().destroy(request, *args, **kwargs)
        return Response(status=status.HTTP_403_FORBIDDEN)

    def partial_update(self,request, *args, **kwargs):
        if request.user == self.get_object().creator :
            return super().partial_update(request, *args, **kwargs)
        return Response(status=status.HTTP_403_FORBIDDEN)



