from django.contrib import admin
from .models import Category,Course,User,Lesson,Tag,Rating,Action,LessonView,LessonComment
from django.utils.html import mark_safe
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
# Register your models here.


class LessonInline(admin.StackedInline):
    model = Lesson
    pk_name = 'course'
class LessonTagInline(admin.TabularInline):
    model = Lesson.tag.through
class CousesInLine(admin.StackedInline):
    model = Course
    pk_name = 'category'

class CategoryAdmin(admin.ModelAdmin):
    inlines = (CousesInLine, )
class CourseAdmin(admin.ModelAdmin):
    inlines = (LessonInline, )
    list_display = ['id','name','created_date','active','avatar','des','category']
    search_fields = ['name','created_date','category__name']
    list_filter = ['category']
    readonly_fields = ['imgShow']
    def imgShow(self,course):
        if course:
            return mark_safe(
                f"<img src='/media/{course.avatar.name}' alt = {course.name} width ='200px' />"
            )

#dùng để upload ảnh trong admin site
class LessonForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget)
    # class Meta:
    #     model = Lesson
    #     fields = '__all__'



class LessonAdmin(admin.ModelAdmin):
    form = LessonForm
    inlines = (LessonTagInline,)
    list_display = ['id','name','created_date','active','avatar','content','course']
    search_fields = ['name','created_date','course__name']
    list_filter = ['course']
    readonly_fields = ['imgShow']
    def imgShow(self,lesson):
        if lesson:
            return mark_safe(
                f"<img src='/media/{lesson.avatar.name}' alt = {lesson.name} width ='200px' />"
            )


admin.site.register(Category,CategoryAdmin)
admin.site.register(Course,CourseAdmin)
admin.site.register(User)
admin.site.register(Lesson,LessonAdmin)
admin.site.register(Tag)
admin.site.register(Rating)
admin.site.register(Action)
admin.site.register(LessonView)
admin.site.register(LessonComment)