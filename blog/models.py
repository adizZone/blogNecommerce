from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


# Create your models here.
class BlogPost(models.Model):
    blog_id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=50, default="")
    title = models.CharField(max_length=100)
    intro = models.CharField(max_length=550)
    whole_content = models.TextField(default='', null=True)
    heading01 = models.CharField(max_length=50, default='', null=True)
    content01 = models.CharField(max_length=5000, default='', null=True)
    heading02 = models.CharField(max_length=50, default="", null=True)
    content02 = models.CharField(max_length=5000, default="", null=True)
    heading03 = models.CharField(max_length=50, default="", null=True)
    content03 = models.CharField(max_length=5000, default="", null=True)
    publish_date = models.DateField(auto_now_add=True)
    image = models.ImageField(upload_to="blog/images", default="", null=True)
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class Comment(models.Model):
    s_no = models.AutoField(primary_key=True)
    your_comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    timeStamp = models.DateTimeField(default=now)

    def __str__(self):
        if self.parent == None:
            return f"A comment by - {self.user.username}: {self.your_comment[:20]}..., Comment number =  {self.s_no}"
        return f"A reply by - {self.user.username}, to Comment number - {self.parent.s_no}: {self.your_comment[:20]}... "