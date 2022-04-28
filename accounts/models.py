from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    email = models.EmailField(blank=True)
    fullname = models.CharField(max_length=100, blank=True)
    address = models.TextField(max_length=300, blank=True)
    img_width = models.IntegerField(null=True, blank=True)
    img_height = models.IntegerField(null=True, blank=True)
    avatar = models.ImageField(
        upload_to="avatars/",
        width_field="img_width",
        height_field="img_height",
        blank=True,
        null=True,
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Community(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=400)
    location = models.TextField(max_length=400)
    img_width = models.IntegerField(null=True, blank=True)
    img_height = models.IntegerField(null=True, blank=True)
    image = models.ImageField(
        upload_to="communityimages/",
        width_field="img_width",
        height_field="img_height",
        blank=True,
        null=True,
    )
    users = models.ManyToManyField(User, through="MemberRole", null=True)

    def __str__(self):
        return f"Community {self.name}"


class MemberRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    ADMIN = 1
    MEMBER = 100
    MEMBER_ROLES = ((ADMIN, "Admin"), (MEMBER, "Member"))
    role = models.IntegerField(choices=MEMBER_ROLES)

    def __str__(self):
        return (
            f"Map {self.user.username} to {self.community.name} with role {self.role}"
        )
