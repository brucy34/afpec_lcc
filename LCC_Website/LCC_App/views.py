from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse 
from .models import Book,Category, Concurrent,Event
from .forms import ConcurrentForm,ConcurrentLoginForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login as auth_login
from django.views.decorators.clickjacking import xframe_options_exempt
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import JsonResponse
from django.db import models
from django.contrib import messages
from django.core.mail import send_mail


def add_to_library(request, book_pk):
    concurrent_id = request.session.get('concurrent_id')
    if concurrent_id:
        try:
            book = Book.objects.get(pk=book_pk)
            concurrent = get_object_or_404(Concurrent, id=concurrent_id)
            if book in concurrent.personal_library.all():
                concurrent.personal_library.remove(book)
                message = 'Book removed from personal library successfully.'
            else:
                concurrent.personal_library.add(book)
                message = 'Book added to personal library successfully.'
            
            if request.is_ajax():
                return JsonResponse({'message': message})
            else:
                # If not an AJAX request, you can redirect the user back to the previous page
                return redirect(request.META.get('HTTP_REFERER'))
        except Book.DoesNotExist:
            if request.is_ajax():
                return JsonResponse({'error': 'Book not found.'})
            else:
                # Handle the non-AJAX response here, for example, redirect or show a message
                pass
    else:
        if request.is_ajax():
            return JsonResponse({'error': 'User not found.'})
        else:
            # Handle the non-AJAX response here, for example, redirect or show a message
            pass




def add_concurrent(request):
    if request.method == 'POST':
        form = ConcurrentForm(request.POST)
        if form.is_valid():
            firstname = form.cleaned_data['firstname']
            lastname = form.cleaned_data['lastname']
            sex = form.cleaned_data['sex']
            in_university = form.cleaned_data['in_university']
            university = form.cleaned_data['university']
            discipline = form.cleaned_data['discipline']
            level = form.cleaned_data['level']
            profession = form.cleaned_data['profession']
            password = form.cleaned_data['password']

            concurrent_code =f"{lastname[:3]}-{firstname[:3]}-24-AFPEC-LCC"
            concurrent = Concurrent.objects.create_user(concurrent_code=concurrent_code,
                firstname=firstname,lastname=lastname,sex=sex,in_university=in_university,university=university,discipline=discipline,level=level,profession=profession,password=password)
            return render(request, 'registration_success.html', {'concurrent_code': concurrent.concurrent_code})
        else:
            print(form.errors)
    else:
        form = ConcurrentForm()
    
    return render(request, 'registration.html', {'form': form})

def list_events(request):
    events = Event.objects.all()
    last_events = Event.objects.all()[:5]
    # Get the user's query from the form
    query = request.GET.get('query')
    # Initialize results variable
    results = None
    if query and query.lower() in ["all", "show all"]:
        # Return all books
        results = events
    elif query:
        # Search by name, author, year, and categories
        results = Event.objects.filter(
            models.Q(title__icontains=query) |
            models.Q(date__icontains=query)
        ).distinct()
        # Save the search query in the user's session
        request.session['search_query'] = query
    else:
        # If no query provided, return all events
        default_events = events[:6]  # Limit to the first 6 events
        # Clear the search query from the user's session
        request.session.pop('search_query', None)

    context = {
        'query': query,
        'results': results if results is not None else default_events,  # Use results if available, otherwise default_books
        'events': events,
        'last_events': last_events
    }

    return render(request, 'events.html', context)


def home(request):
    categories = Category.objects.all()
    list_events = Event.objects.all()[::-1][:3]
    if request.method == 'POST':
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        tel = request.POST.get('tel')
        email = request.POST.get('email')
        message = request.POST.get('message')
    
        # Compose the email
        subject = f"Un mail de {nom} {prenom}"
        message_body = f"\n{message}\n\n\n"
        message_body += f"{nom}\n"
        message_body += f"{prenom}\n"
        message_body += f"Téléphone: {tel}\n"
        message_body += f"Email: {email}\n"
        

        # Send the email
        recipient_email = 'afpechaiti@yahoo.com'
        try:
            send_mail(subject, message_body, email, [recipient_email], fail_silently=False)
        except Exception as e:
            messages.error(request, f'Email sending failed: {str(e)}')

        # Redirect to a success page
        return redirect('LCC_App:home') 
           
    return render(request, 'index.html', {'categories': categories, 'list_events': list_events})

def connect(request):
    if request.method == 'POST':
        form = ConcurrentLoginForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            password = form.cleaned_data['password']
            concurrent = authenticate(request, code=code, password=password)
            if concurrent is not None:
                auth_login(request, concurrent)
                request.session['concurrent_id'] = concurrent.id
                redirect_url = reverse('LCC_App:list_books') + f'?user_id={concurrent.id}'
                return HttpResponseRedirect(redirect_url)
            else:
                form.add_error(None, "Invalid ID or password.")
    else:
        form = ConcurrentLoginForm()

    return render(request, 'login.html', {'form': form})





@xframe_options_exempt
def view_pdf(request, pk):
    # Replace 'YourModel' with the actual model where your PDFs are stored
    pdf_object = get_object_or_404(Book, pk=pk)

    # Set the response content type to 'application/pdf'
    response = HttpResponse(pdf_object.pdf.read(), content_type='application/pdf')
    
    # Set the 'X-Frame-Options' header to allow embedding
    response['X-Frame-Options'] = 'SAMEORIGIN'
    
    return response

def search_books(request):
    # Get the user's query from the form
    query = request.GET.get('query')
    # user_id = request.GET.get('user_id')
    user_id= request.session.get('concurrent_id')
    concurrent=None
    # Initialize results variable
    results = None
    # Get all categories
    categories = Category.objects.all()

    if user_id:
        concurrent = get_object_or_404(Concurrent, id=user_id)

    if query and query.lower() in ["all", "show all"]:
        # Return all books
        results = Book.objects.all()
    elif query and query.lower() in ["my library", "personal library"]:
        results = concurrent.personal_library.all()
    elif query:
        # Search by name, author, year, and categories
        results = Book.objects.filter(
            models.Q(title__icontains=query) |
            models.Q(author__icontains=query) |
            models.Q(year__icontains=query) |
            models.Q(category__name__icontains=query)
        ).distinct()
        # Save the search query in the user's session
        request.session['search_query'] = query
    else:
        # If no query provided, return all books
        default_books = Book.objects.all()[:10]  # Limit to the first 10 books
        # Clear the search query from the user's session
        request.session.pop('search_query', None)

    context = {
        'query': query,
        'results': results if results is not None else default_books,  # Use results if available, otherwise default_books
        'user':concurrent,
        'categories': categories
    }
    
    return render(request, 'library.html', context)


def logout(request):
    user_id= request.session.get('concurrent_id')
    if user_id:
        request.session.flush()
        return redirect('LCC_App:list_books')