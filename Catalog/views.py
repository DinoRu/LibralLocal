import datetime
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse
from .forms import RenewBookForm
from .models import( 
    Book, BookInstance,
     Author, Genre)


def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()
    num_genres = Genre.objects.all().count()
    num_titles = Book.objects.filter(title__exact='Horreur').count()
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genres': num_genres,
        'num_titles': num_titles,
        'num_visits': num_visits,
    }

    return render(request, 'index.html', context=context)


class BookListView(ListView):
    model = Book
    paginate_by = 3
    

class BookDetailView(DetailView):  
    model = Book                                          


class AuthorListView(ListView):
    model = Author


class AuthorDetailView(DetailView):
    model = Author


class LoanedBooksByUserListView(LoginRequiredMixin, ListView):
    models = BookInstance
    template_name = "catalog/bookinstance_list_borrowed_user.html"
    paginate_by = 3

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')
        

class AllBookUsersBorrowed(LoginRequiredMixin, ListView):
    models = BookInstance
    template_name = "catalog/bookinstance_user_borrowed.html"
    paginate_by = 3

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o')
        

class MyView(PermissionRequiredMixin, View):
    permission_required = 'Catalog.can_mark_returned'
    

@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librairian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # Si la request est "POST" traité les données
    if request.method == 'POST':

        # Créez une instance de formulaire et remplissez-la avec les données de la requête (liaison):
        form = RenewBookForm(request.POST)

        # Verifier si le formulaire est valide:
        if form.is_valid():
            # On efface les donnees apres une soumission
            book_instance.due_back = form.cleaned_data['renewal_date']
            # Sauvegarde les données du formulaire
            book_instance.save()

            #Redirige l'utilisateur vers un nouvel url
            return HttpResponseRedirect(reverse('Catalog:all-borrowed'))
    
    # Si c'est la methode GET ou un autre methode creer un formulaire vide
    else:
        proposed_renewal_date = datetime.date.today() - datetime.timedelta(weeks=4)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})
    
    context = {
        'form': form,
        'book_instance': book_instance,
    }
    return render(request, 'catalog/book_renew_librarian.html', context=context)