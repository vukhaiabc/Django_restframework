from  .models import Course,Tag,Lesson,Category,User,Rating,Action,LessonView,LessonComment
from rest_framework.serializers import ModelSerializer

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','password','first_name','last_name','email','avatar']
        extra_kwargs = {
            'password': {
                'write_only' : True
            }
        }

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
class CategorySerializer(ModelSerializer):
    class Meta :
        model = Category
        fields = ["id","name"]

class CourseSerializer(ModelSerializer):
    # category = CategorySerializer()
    class Meta :
        model = Course
        fields = ["id","name","avatar","created_date","category"]

class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields =['id','name']

class LessonSerializer(ModelSerializer):
    class Meta :
        model = Lesson
        fields = ["id","name","avatar","created_date","course"]

class LessonDetailSerializer(LessonSerializer):
    tag = TagSerializer(many=True)
    class Meta :
        model = LessonSerializer.Meta.model
        fields = LessonSerializer.Meta.fields + ['content','tag']

class LessonCommentSerializer(ModelSerializer):
    class Meta :
        model = LessonComment
        fields = ['id','content','creator','lesson','created_date']

class ActionSerializer(ModelSerializer):
    class Meta:
        model = Action
        fields = ['id','created_date', 'lesson','type','creator']

class RatingSerializer(ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id','created_date', 'lesson','rate','creator']

class LessonViewSerializer(ModelSerializer):
    class Meta:
        model = LessonView
        fields = ['id','views','lesson']