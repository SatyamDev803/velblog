from django.shortcuts import render, HttpResponse
from home.models import Contact
from django.contrib import messages
from blog.models import Post

# Create your views here.
def home(request):
    # Fetching the latest 4 posts to display as popular posts
    popular_posts = Post.objects.order_by('-timeStamp')[:4]
    context = {'popular_posts': popular_posts}
    return render(request, 'home/home.html', context)

def about(request):
    return render(request, 'home/about.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']
        if len(name)<2 or len(email)<3 or len(phone)<10 or len(content)<4:
            messages.error(request, "Input Correct Details!")
        else:
            contact = Contact(name=name, email=email, phone=phone, content=content)
            contact.save()
            messages.success(request, "Contact Details has been sent!")

    return render(request, 'home/contact.html')

def search(request):
    query = request.GET.get('query', '').strip()  
    if not query or len(query) > 78:
        allPosts = Post.objects.none 
    else:
        allPostsTitle = Post.objects.filter(title__icontains=query)
        allPostsContent = Post.objects.filter(content__icontains=query)
        allPosts = allPostsTitle.union(allPostsContent)

    if allPosts.count() == 0:
            messages.warning(request, "No search results found.")
    params = {'allPosts': allPosts, 'query': query}
    return render(request, 'home/search.html', params)

