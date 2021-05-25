from django.views.generic.edit import FormView
from django.views.generic.list import ListView

from .forms import TransactionForm
from .models import CustomUser


class TransactionView(FormView):
    form_class = TransactionForm
    template_name = 'transaction.html'
    success_url = '/usersaccounts/'

    def form_valid(self, form):
        form.process_transaction()
        return super().form_valid(form)


class UserAccountsView(ListView):
    model = CustomUser
    template_name = 'useraccounts.html'

