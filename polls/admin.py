from django.contrib import admin
from .models import Question,Choice,Blog,Entry,Author
# Register your models here.
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Blog)
admin.site.register(Entry)
admin.site.register(Author)
