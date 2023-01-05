from django.shortcuts import render,redirect
from.import models
from.models import User,Book
from django.contrib import messages



def index(request):
    return render(request,'index.html')

def register(request):
    name=request.POST['Name']
    alias=request.POST['alias']
    email=request.POST['Email']
    password=request.POST['password']
    confirmpw=request.POST['cpassword']
    if request.method=='POST':
        errors = User.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            models.Add_user(name,alias,email,password,confirmpw)
            return redirect('/')

def login(request):
    email=request.POST['Email']
    password=request.POST['password']
    if models.Login(email,password,request):
       return redirect('/books')
    else:
        return redirect('/')

def books(request):
    context={
        'user':models.users(request),
        'books':models.get_all_book(),
    }
    return render (request,'books.html',context)

def addBook(request):
    context={
        'authorlist':models.get_authors()
    }
    print(context)

    return render(request,'addbook.html',context)
    

def addprocess(request):
    book_title=request.POST['btitle']
    author_from_user=request.POST['newauthor']
    author_from_list=request.POST['authorlist']
    content=request.POST['reviewbox']
    rating=request.POST['stars']
    if request.POST['authorlist'] != ' ':
        author = models.Get_Author(int(author_from_list))
    else:
        author_id = models.Add_Author(author_from_user).id
        author = models.Get_Author(author_id)
    if request.method=='POST':
        errors=Book.objects.book_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/addBook')
        else:
            book= models.add_Book(book_title,author)
            bookId = book.id
            models.add_review(content,rating,request,book_id = bookId)
            # request.session['bookid'] =bookId
            return redirect('/books/'+str(bookId))

def view(request,new_book_id):
    bookId=new_book_id
    context={
        'book':models.get_book(bookId)
        
    }
    return render (request,'viewbook.html',context)

def addReview(request):
    id= request.session['userid']
    Book_id=request.POST['view_book_id']
    content=request.POST['reviewbox']
    rating=request.POST['stars']

    if request.method=='POST':
        models.add_Review(id,Book_id,content,rating)
        return redirect('/books/'+str(Book_id))


def delete(request):
    id=request.POST['review_id']
    bookid=request.POST['book_id']
    models.delete_review(id)
    return redirect('/books/'+str(bookid))

def userview(request,userID):
    
    num_of_reviews=models.Get_number_of_Reviews_for_user(userID)
    context={
        'user':models.Get_User(userID),
        "num_of_reviews" : num_of_reviews,
    }
    return render(request,'user.html',context)