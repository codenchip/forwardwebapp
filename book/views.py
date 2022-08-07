from django.shortcuts import render, redirect
from book.models import Book
from book.forms import BookForm
from django.http import HttpResponse

# Create your views here.
def index(request):
    shelf = Book.objects.all()
    return render(request,'book/library.html',{"shelf":shelf})

def create(request):
    book_form = BookForm()
    if request.method == 'POST':
        book_form = BookForm(request.POST,request.FILES)
        if book_form.is_valid():
            book_form.save()
            return redirect('index')
        else:
            return HttpResponse("Something wrong with your form!")
    else:
        return render(request, 'book/upload_form.html',{'book_form':book_form})

def update_book(request, book_id):
    book_id = int(book_id)
    
    try:
        book_query = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        return redirect('index')
    
    book_form = BookForm(request.POST or None, instance = book_query) 
    if book_form.is_valid():
        book_form.save()
        return redirect('index')
    
    return render(request,'book/upload_form.html',{'book_form':book_form})

def delete_book(request, book_id):
    book_id = int(book_id)
    try:
        book_query = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        return redirect('index')
        
    book_query.delete()
    return redirect('index')