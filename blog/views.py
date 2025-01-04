from django.shortcuts import render, redirect
from blog.models import Post, BlogComment
from django.contrib import messages

# Create your views here.
def blogHome(request):
    allPosts = Post.objects.order_by('-timeStamp').all()
    context = {'allPosts': allPosts}
    return render(request, 'blog/blogHome.html', context)

def blogPost(request, slug):
    post = Post.objects.filter(slug=slug).first()
    post.views = post.views + 1
    post.save()
    comments = BlogComment.objects.filter(post=post, parent__isnull=True).order_by('-timestamp')  
    replies = BlogComment.objects.filter(post=post).exclude(parent__isnull=True).order_by('parent__timestamp')  

    context = {
        'post': post,
        'comments': comments,
        'replies': replies,
        'user': request.user,
    }
    return render(request, 'blog/blogPost.html', context)

def postComment(request):
    if request.method == 'POST':
        comment = request.POST.get('comment')  # The comment text
        user = request.user  # The logged-in user
        postSno = request.POST.get('sno')  # Post identifier
        parentSno = request.POST.get('parentSno')  # Parent comment identifier (optional)

        # Validate `postSno`
        if not postSno:
            messages.error(request, "Invalid post reference.")
            return redirect('/blog/')

        try:
            post = Post.objects.get(sno=postSno)
        except Post.DoesNotExist:
            messages.error(request, "The post you are trying to comment on does not exist.")
            return redirect('/blog/')

        # Validate Comment 
        if not comment or comment.strip() == "":
            messages.warning(request, "Comment cannot be empty.")
            return redirect(f"/blog/{post.slug}")

        # Determine if this is a new comment or a reply
        if parentSno == "" or parentSno is None:
            new_comment = BlogComment(comment=comment, user=user, post=post)
            new_comment.save()
            messages.success(request, "Your comment has been posted")  # Only show this for a new comment
        else:
            try:
                parent = BlogComment.objects.get(sno=parentSno)
                new_comment = BlogComment(comment=comment, user=user, post=post, parent=parent)
                new_comment.save()
                messages.success(request, "Your reply has been posted.")  # Only show this for a reply
            except BlogComment.DoesNotExist:
                messages.error(request, "The parent comment does not exist.")
                return redirect(f"/blog/{post.slug}")

        return redirect(f"/blog/{post.slug}")