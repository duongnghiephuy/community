from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DeleteView

from .forms import PostForm
from .models import Order, Post
from django.utils import timezone

# Create your views here.


class NewPost(View):
    def get(self, request):
        form = PostForm(request.user)
        return render(request, "posts/post_form.html", {"form": form})

    def post(self, request):

        form = PostForm(request.user, request.POST, request.FILES)
        if form.is_valid():
            community_id = int(request.POST.get("community", ""))
            if not request.user.community_set.filter(id=community_id).exists():
                return render(
                    request,
                    "posts/post_form.html",
                    {"form": form, "permissionerror": "You are not in the community"},
                )
            new_post = form.save()
            Order.objects.create(
                post=new_post, participant=request.user, role=Order.HOST
            )
            return render(request, "posts/success.html")
        else:
            return render(request, "posts/post_form.html", {"form": form})


class PostListView(ListView):
    model = Post
    template_name = "posts/index.html"
    paginate_by = 5

    def get_queryset(self):
        return Post.objects.filter(
            community__in=self.request.user.community_set.all(),
            schedule_to__gte=timezone.now(),
        ).order_by("-updated_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = PostForm(self.request.user)
        context["form"] = form
        context["communities"] = self.request.user.community_set.all()
        return context


class UpdateOrder(View):
    def get(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        if request.user in post.participants.all():
            Order.objects.get(post=post, participant=request.user).delete()
            return render(request, "posts/participate.html", {"post": post})
        else:
            Order.objects.create(post=post, participant=request.user, role=Order.SHARER)
            return render(request, "posts/unparticipate.html", {"post": post})


class DeletePost(View):
    def delete(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        if request.user == post.host:
            post.delete()
            return render(request, "posts/success.html")
        else:
            return render(request, "community/invalid_request.html")


class AsynUpdatePost(View):
    def get(self, request):
        post = Post.objects.filter(
            order__participant=request.user, order__role=Order.HOST
        ).latest("created_at")
        return render(request, "posts/asynpost.html", {"post": post})


class ScheduleList(ListView):
    model = Post
    template_name = "posts/schedule.html"
    paginate_by = 5

    def get_queryset(self):
        return Post.objects.filter(order__participant=self.request.user)


class HostList(ListView):
    model = Post
    template_name = "posts/schedule_host.html"
    paginate_by = 1

    def get_queryset(self):
        return Post.objects.filter(
            order__participant=self.request.user, order__role=Order.HOST
        )


class ShareList(ListView):
    model = Post
    template_name = "posts/schedule_share.html"
    paginate_by = 5

    def get_queryset(self):
        return Post.objects.filter(
            order__participant=self.request.user, order__role=Order.SHARER
        )
