from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from django.views.generic import CreateView, ListView, UpdateView, DetailView, FormView
from django.template import loader
from django.urls import reverse_lazy
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import auth
from django.contrib.auth import login, authenticate
from allauth.socialaccount.models import SocialAccount
from django.core.exceptions import ObjectDoesNotExist


from p_library.models import Book, Publisher, Author, Friend, UserProfile
from p_library.forms import AuthorForm, BookForm, FriendForm, FriendEditForm, ProfileCreationForm, \
    UserProfileUpdateForm


def books_list(request):
    books = Book.objects.all()
    return HttpResponse(books)


def index(request):
    template = loader.get_template('index.html')
    books = Book.objects.all()
    data = {
        'title': 'мою библиотеку',
        'books': books,
    }
    if request.user.is_authenticated:
        data['username'] = request.user.username
    return HttpResponse(template.render(data, request))


def book_increment(request):
    if request.method == 'POST':
        book_id = request.POST['id']
        if not book_id:
            return redirect('/index/')
        else:
            book = Book.objects.filter(id=book_id).first()
            if not book:
                return redirect('/index/')
            book.copy_count += 1
            book.save()
        return redirect('/index/')
    else:
        return redirect('/index/')


def book_decrement(request):
    if request.method == 'POST':
        book_id = request.POST['id']
        if not book_id:
            return redirect('/index/')
        else:
            book = Book.objects.filter(id=book_id).first()
            if not book:
                return redirect('/index/')
            if book.copy_count < 1:
                book.copy_count = 0
            else:
                book.copy_count -= 1
            book.save()
        return redirect('/index/')
    else:
        return redirect('/index/')


def publishers_list(request):
    template = loader.get_template('publishers.html')
    publishers = Publisher.objects.all()

    book_publisher = {}
    for p in publishers:
        book_publisher[p.name] = Book.objects.filter(publisher=p)

    data = {
        'publishers': publishers,
        'book_publisher': book_publisher,
        'user': request.user,
    }
    if request.user.is_authenticated:
        data['username'] = request.user.username
    return HttpResponse(template.render(data))


def user(request, pk):

    data = {
        'user': request.user,
        'username': request.user.username,
    }
    try:
        template = loader.get_template('github_user.html')
        data['extra_data'] = SocialAccount.objects.get(provider='github', user=request.user).extra_data
        return HttpResponse(template.render(data))
    except ObjectDoesNotExist:
        pass

    try:
        template = loader.get_template('user.html')
        data['extra_data'] = UserProfile.objects.get(user=request.user)
        return HttpResponse(template.render(data))
    except ObjectDoesNotExist:
        return HttpResponse(template.render(data))


class AuthorEdit(CreateView):
    model = Author
    form_class = AuthorForm
    success_url = reverse_lazy('p_library:author_list')
    template_name = 'author_edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['username'] = self.request.user.username
        return context


class AuthorList(ListView):
    model = Author
    template_name = 'authors_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['username'] = self.request.user.username
        return context


class BookEdit(CreateView):
    model = Book
    form_class = BookForm
    success_url = reverse_lazy(index)
    template_name = 'book_edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['username'] = self.request.user.username
        return context


class FriendList(ListView):
    model = Friend
    template_name = 'friends_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['username'] = self.request.user.username
        return context


class FriendUpdate(UpdateView):
    model = Friend
    form_class = FriendForm
    success_url = reverse_lazy('p_library:friend_list')
    template_name = 'friend_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['username'] = self.request.user.username
        return context


class FriendEdit(CreateView):
    model = Friend
    form_class = FriendEditForm
    success_url = reverse_lazy('p_library:friend_list')
    template_name = 'friend_edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['username'] = self.request.user.username
        return context


class BookDetailView(DetailView):

    model = Book
    template_name = 'book_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['username'] = self.request.user.username
        return context


class RegisterView(FormView):

    form_class = UserCreationForm

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password1')
        login(self.request, authenticate(username=username, password=raw_password))
        return super(RegisterView, self).form_valid(form)


class CreateUserProfile(FormView):

    form_class = ProfileCreationForm
    template_name = 'profile-create.html'
    success_url = reverse_lazy('index')

    def dispatch(self,  request, *args, **kwargs):
        if self.request.user.is_anonymous:
            return HttpResponseRedirect(reverse_lazy('login'))
        return super(CreateUserProfile, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.save()
        return super(CreateUserProfile, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['username'] = self.request.user.username
            context['bttntxt'] = 'Создать'
            context['message'] = 'Создать профиль'
        return context


class UserProfileUpdate(UpdateView):
    model = UserProfile
    template_name = 'profile-create.html'
    form_class = UserProfileUpdateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['username'] = self.request.user.username
            context['bttntxt'] = 'Редактировать'
            context['message'] = 'Изменить данные'
        return context

    def get_success_url(self):
        return reverse_lazy('p_library:user', args=(self.request.user.pk,))
