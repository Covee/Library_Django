from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Author    


def index(request):
	num_books = Book.objects.all().count()
	num_instances = BookInstance.objects.all().count()
	num_instances_available = BookInstance.objects.filter(status__exact='a').count()
	num_authors = Author.objects.count()
	num_visits = request.session.get('num_visits', 0)
	request.session['num_visits'] = num_visits + 1

	return render(
		request,
		'index.html',
		context = {'num_books':num_books, 'num_instances':num_instances,
					'num_instances_available':num_instances_available,
					'num_authors':num_authors, 'num_visits':num_visits}
		)


from django.views import generic


class BookListView(generic.ListView):
	model = Book
	# context_object_name = 'book_list'
	# queryset = Book.objects.filter
	# template_name = 'books/my_arbitary_template_name_list.html'


class BookDetailView(generic.DetailView):
	model = Book


# 이 ListView를 넣어주면서, perms를 쓰기 위해 html에서 {% author_list %} 로 가져다 쓸 수 있음
class AuthorListView(generic.ListView):
	model = Author


class AuthorDetailView(generic.DetailView):
	model = Author


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
	model = BookInstance
	template_name = 'catalog/bookinstance_list_borrowed_user.html'
	paginate_by = 10

	def get_queryset(self):
		return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


from django.contrib.auth.mixins import PermissionRequiredMixin

class LoanedBooksAllListView(PermissionRequiredMixin, generic.ListView):
	model = BookInstance
	permission_required = 'catalog.can_mark_returned'
	template_name = 'catalog/bookinstance_list_borrowed_all.html'
	paginate_by = 10

	def ger_queryset(self):
		return BookInstance.objects.filter(status__exact='o').order_by('due_back')


from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime

from .forms import RenewBookForm

def renew_book_librarian(request, pk):
	book_inst = get_object_or_404(BookInstance, pk = pk)

	if request.method == 'POST':
		form = RenewBookForm(request.POST)

		if form.is_valid():
			book_inst.due_back = form.cleaned_data['renewal_date']
			book_inst.save()

			return HttpResponseRedirect(reverse('all-borrowed') )

	else:
		proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=2)
		form = RenewBookForm(initial={'renewal_date': proposed_renewal_date,})

	return render(request, 'catalog/book_renew_librarian.html', {'form': form, 'bookinst':book_inst})



class AuthorCreate(PermissionRequiredMixin, CreateView):
	model = Author
	fields = '__all__'
	# initial = {'date_of_death':'12/10/2016',}
	permission_required = ('catalog.create_author')

	# def get_context_data(self, **kwargs):
	# 	context = super(AuthorCreate, self).get_context_data(**kwargs)
	# 	context['action'] = reverse('author-create')

	# 	return context


class AuthorUpdate(PermissionRequiredMixin, UpdateView):
	model = Author
	fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
	permission_required = ('catalog.update_author')
	

	# def get_context_data(self, **kwargs):
	# 	context = super(AuthorUpdate,self).get_context_data(**kwargs)
	# 	context['action'] = reverse('author-update', kwargs={'pk':self.get_object().id})
	# 	return context


class AuthorDelete(PermissionRequiredMixin, DeleteView):
	model = Author
	success_url = reverse_lazy('authors')
	permission_required = ('catalog.delete_author')

