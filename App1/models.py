from django.db import models
import re
import bcrypt

class UserManager(models.Manager):
    def basic_validator(self,postData):
        error={}
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        password_regex =re.compile(r'^[a-zA-Z0-9.+_-]')
        special_symbols = ['$','@','#','%','^','&']
        if len(postData['Name']) < 3 :
            error['Name'] = " name should be at least 3 characters"
        if len(postData['alias']) < 3 :
            error['alias'] = "alias should be at least 3 characters"
        if not email_regex.match(postData['Email']) :
            error['Email'] = "invaild email"
        if len(postData['password']) < 6:
            error['password_less_than'] = "Password must have atleast 6 characters"
        if len(postData['password']) > 20 :
            error['password_grather_than'] = "'Password cannot have more than 20 characters"
        if not any(characters.isupper() for characters in postData['password']):
            error['password_notInclude_upper'] = "Password must have at least one uppercase character"
        if not any(characters.islower() for characters in postData['password']):
            error['password_notInclude_lower'] = "Password must have at least one lowercase character"
        if not any(characters.isdigit() for characters in postData['password']):
            error['password_notInclude_number'] = "Password must have at least one numeric character."
        if not any(characters in special_symbols for characters in postData['password']):
            error['password_symbol'] = "Password should have at least one of the symbols $@#%^&"
        return error



    def book_validator(self, postData):
        error = {}
        if len(postData['btitle']) <3:
            error['btitle'] = "book title should be at least 3 characters"
        if (len(postData['authorlist']) == 0 ) and (len(postData['newauthor']) == 0) :
            error['not_fill_author'] = "please select or insert author name"

        if len(postData['reviewbox']) < 3 :
            error['review'] = "please insert your opinion in this book"
        return error

class ReviewManager(models.Manager):
    def book_validator(self, postData):
        errors = {}
        if len(postData['reviewbox']) < 1:
            errors["reviewbox"] = "Review should not be empty"
        return errors




class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    confirmpw=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    objects=UserManager()

def Get_User(UserId):
    return User.objects.get(id = UserId)

def Add_user(name,alias,email,password,confirmpw):
    name=name
    alias=alias
    email=email
    password=password
    confirmpw=confirmpw
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    if(confirmpw==password):
        return User.objects.create(name=name,alias=alias,email=email,password=pw_hash)

def Login(email,password,request):
    email=email
    password=password
    user = User.objects.filter(email = email)
    if user:
        loged_user = user[0]
        if bcrypt.checkpw(password.encode(), loged_user.password.encode()):
            request.session['userid'] = loged_user.id
            return True

def users(request):
    id=request.session['userid']
    return User.objects.get(id=id)

class Author(models.Model):
    name = models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    #books=alist of the the booke created by the author
def Add_Author(author):
    return Author.objects.create(name=author)

def get_authors():
    return Author.objects.all()

def Get_Author(author_from_list_id):
    return Author.objects.get(id=author_from_list_id)


class Book(models.Model):
    book_title = models.CharField(max_length=255)
    author = models.ForeignKey(Author , related_name="books" , on_delete=models.DO_NOTHING)
    created_at=models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

def add_Book(book_title,author):
    book_title=book_title
    author = author
    return Book.objects.create(book_title=book_title,author=author)

def get_book(bookId):
    return Book.objects.get(id=bookId)

def get_all_book():
    return Book.objects.all()
class Review(models.Model):
    content = models.TextField()
    rating = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name="reviews" , on_delete=models.CASCADE)
    book = models.ForeignKey(Book, related_name="reviews" , on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

def add_review(content,rating,request,book_id):
    # book_title=book_title
    id=request.session['userid']
    book=Book.objects.get(id= book_id)
    user=User.objects.get(id=id)
    content=content
    rating=rating
    return Review.objects.create(content=content,rating=rating,user=user,book=book)


def add_Review(id,Book_id,content,rating):
    user=User.objects.get(id=id)
    book=Book.objects.get(id=Book_id)
    return Review.objects.create(content=content,rating=rating,user=user,book=book)

def delete_review(id):
    review=Review.objects.get(id=id)
    return review.delete()

def Get_number_of_Reviews_for_user( UserId):
    count = 0
    reviews = Review.objects.filter(user = UserId)
    for one in reviews :
        count += 1
        print("$$$ " ,count)

    return count
