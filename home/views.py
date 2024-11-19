from django.shortcuts import render, HttpResponse, redirect
from home.models import Contact
from django.contrib import messages
from blog.models import Post
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# Create your views here.

# HTML Pages
def home(request):
    # Fetching the latest 4 posts to display as popular posts
    popular_posts = Post.objects.order_by('-views')[:4]
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
    query = request.GET.get('query', '').strip()  # Get the search query and strip extra spaces
    if not query:  # Check if the query is empty
        messages.warning(request, "Search query cannot be empty.")  # Show a warning message
        return redirect('home')  # Redirect to the home page or any relevant page
    
    if len(query) > 78:  # Validate the query length
        messages.warning(request, "Search query is too long.")
        return redirect('home')  # Redirect to prevent further processing

    # Perform search only if the query is valid
    allPostsTitle = Post.objects.filter(title__icontains=query)
    allPostsContent = Post.objects.filter(content__icontains=query)
    allPosts = allPostsTitle.union(allPostsContent)

    if not allPosts.exists():  # Check if there are no results
        messages.warning(request, "No search results found.")
    
    params = {'allPosts': allPosts, 'query': query}
    return render(request, 'home/search.html', params)


# Authentication APIs 
def handleSignup(request):
    if request.method == 'POST':
    #   Get the post parameters
        username = request.POST['username']  
        fname = request.POST['fname']  
        lname = request.POST['lname']  
        email = request.POST['email']  
        password1 = request.POST['password1']  
        password2 = request.POST['password2']  

        # Check for erroeneous inputs
        if len(username) > 10:
            messages.error(request, "Username must be under 10 chracters")
            return redirect('home')
        
        if not username.isalnum():
            messages.error(request, "Username should only contain letters and numbers")
            return redirect('home')
        
        if password1 != password2:
            messages.erroe(request, "Passwords do no match")
            return redirect('home')
        
        # Create the user
        myuser = User.objects.create_user(username, email, password1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, "Your VelBlog account has been successfully created")
        return redirect('home')

    else:
        return HttpResponse('404 - Not Found')


def handleLogin(request):
    if request.method == 'POST':
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword'] 
        user = authenticate(username=loginusername, password=loginpassword)

        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect('home')
        else:
            messages.error(request, "Invalid Credentials, Please try again")
            return redirect('home')
    return HttpResponse('404 - Not Found')

def handleLogout(request):
    logout(request)
    messages.success(request, "Successfully Logged Out")
    return redirect('home')


