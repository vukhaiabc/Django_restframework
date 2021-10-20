from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField

class User(AbstractUser):
    avatar = models.ImageField(upload_to='avatar/')

    def __str__(self):
        return self.email
class Category(models.Model):
    name = models.CharField(max_length=255,null=False)

    def __str__(self):
        return self.name

class ItemBase(models.Model):
    class Meta:
        abstract = True
    name = models.CharField(max_length=255, null=False)
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    avatar = models.ImageField(upload_to='courses/',default=None)

class Tag(models.Model):
    name = models.CharField(max_length=100,unique=True)
    def __str__(self):
        return self.name

class Course(ItemBase):
    class Meta:
        ordering = ['name']
        unique_together =('name','category')
    des = models.TextField(null= True, blank= True)
    category = models.ForeignKey(Category,on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

class Lesson(ItemBase):
    class Meta:
        ordering = ['id']
        unique_together = ('name', 'course')
    content = RichTextField(default=None)
    course = models.ForeignKey(Course, on_delete=models.CASCADE,related_name="lessons")
    tag = models.ManyToManyField(Tag,blank=True,null=True,related_name='tags')

    def __str__(self):
        return self.name

class LessonComment(models.Model):
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    content = models.TextField(default = None)
    lesson = models.ForeignKey(Lesson,on_delete=models.CASCADE)
    creator = models.ForeignKey(User,on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return self.content
class BaseAction(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    lesson = models.ForeignKey(Lesson,on_delete=models.CASCADE,blank=False)
    creator = models.ForeignKey(User,on_delete=models.CASCADE)

    class Meta :
        abstract = True

class Action(BaseAction):
    like,haha,angry = range(0,3)
    actions = [
        (like,'like'),
        (haha,'haha'),
        (angry,'angry')
    ]
    type = models.PositiveSmallIntegerField(choices=actions,default=like)

    def __str__(self):
        return self.lesson.name

class Rating(BaseAction):
    rate = models.PositiveSmallIntegerField(default=0)
    def __str__(self):
        return "%s, %s"%(self.lesson.name,self.creator.username)

class LessonView(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    lesson = models.OneToOneField(Lesson,on_delete=models.CASCADE)
    views = models.IntegerField(default=0)

    def __str__(self):
        return "%s, %s" % (self.lesson.name, self.views)




