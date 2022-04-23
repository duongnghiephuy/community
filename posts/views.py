from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from .forms import PostForm
from .models import Order

# Create your views here.


class NewPost(View):
    def get(self, request):
        form = PostForm(request.user)
        return render(request, "posts/index.html", {"form": form})

    def post(self, request):
        print(request.FILES["post_image"])
        print(request.POST["group"])
        form = PostForm(request.user, request.POST, request.FILES)
        if form.is_valid():
            new_post = form.save()
            Order.objects.create(
                post=new_post, participant=request.user, role=Order.HOST
            )
            return redirect(reverse_lazy("posts:index-view"))
        else:
            return render(request, "posts/index.html", {"form": form})
