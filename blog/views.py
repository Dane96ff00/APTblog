from django.shortcuts import redirect
from django.shortcuts import render
from django.utils import timezone
from .models import Post, Comment
from django.shortcuts import render, get_object_or_404
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required

#define QuerySet for the Post_list page
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date') #sorting the post in the postlist by "newest first"
    return render(request, 'blog/post_list.html', {'posts': posts})

#define QuerySet for the Post_detail page
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)                                       #showing an error page if a post is not available
    return render(request, 'blog/post_detail.html', {'post': post})

#define QuerySet for the post_new page/template
@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_new.html', {'form': form})

#define QuerySet for the post_edit page/template
@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)                                       #showing an error page if a post is not available
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

#define QuerySet for the post_draft_list page
@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date') #sorting the post in the postlist by "oldest first"
    return render(request, 'blog/post_draft_list.html', {'posts': posts})

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)                                       #showing an error page if a post is not available
    post.publish()                                                              #publish the post
    return redirect('post_detail', pk=pk)

@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)                                       #showing an error page if a post is not available
    post.delete()                                                               #delet the post
    return redirect('post_list')

#define QuerySet for the adding a new comment
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            if request.user.is_authenticated:                                   #audjusing the name of the comment poster to..
                comment.author = request.user                                   #..the user name, if a registerd user is posting
            else:
                comment.author = "GAST : " + comment.author                     #.."GAST : typed Author name" if a not registerd user is posting
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})

#define QuerySet
@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)                                 #showing an error page if a post is not available
    comment.approve()                                                           #publish the comment
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)                                 #showing an error page if a post is not available
    comment.delete()                                                            #delete the comment
    return redirect('post_detail', pk=comment.post.pk)
