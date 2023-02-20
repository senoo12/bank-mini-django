from django import forms
from siswa.models import Rekening, Transaction

class TransactionForm(forms.ModelForm):
    user_from = forms.ModelChoiceField(queryset=Rekening.objects.all(), label='Dari')
    user_to = forms.ModelChoiceField(queryset=Rekening.objects.all(), label='Ke')
    transaction_type = forms.ChoiceField(choices=Transaction.TRANSACTION_TYPE[:2])

    class Meta:
        model = Transaction
        fields = ['user_from', 'user_to', 'transaction_type', 'amount']

class TransferForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['user_from', 'user_to', 'amount']