from telnetlib import STATUS
from django.db import models
from django.contrib.auth.models import User, Group


class Post(models.Model):

    post_title = models.CharField(max_length=300)
    post_content = models.TextField()
    img_width = models.IntegerField()
    img_height = models.IntegerField()
    post_image = models.ImageField(
        upload_to="postimages/", width_field="img_width", height_field="img_height"
    )
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    schedule_from = models.DateTimeField()
    schedule_to = models.DateTimeField()
    participants = models.ManyToManyField(User, through="Order")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def host(self):
        return self.order_set.get(role=Order.HOST).participant

    def __str__(self):
        return self.post_title


class Order(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    participant = models.ForeignKey(User, on_delete=models.CASCADE)
    HOST = 1
    SHARER = 100
    PARTICIPANT_ROLES = ((HOST, "Host"), (SHARER, "Sharer"))
    role = models.IntegerField(choices=PARTICIPANT_ROLES)

    def __str__(self):
        return f"Post {str(self.post)} with {str(self.participant)} and role {str(self.role)}"
