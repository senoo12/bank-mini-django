from django.contrib import admin
from siswa.forms import TransactionForm
from siswa.models import ProfileUser, Rekening, Transaction, History
from import_export.admin import ImportExportModelAdmin
from django.core.exceptions import ValidationError

@admin.register(ProfileUser)
class ProfileUserAdmin(admin.ModelAdmin):
    pass

class TransactionAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'transaction_type', 'amount', 'date', 'user_from_id', 'user_to_id')
    list_filter = ('user_from_id', 'user_to_id')
    form = TransactionForm

    def validate_saldo(self, request, obj, form, change):
        if obj.user_to.saldo < obj.amount:
            raise ValidationError("saldo tidak cukup")
        else:
            def save_model(self, request, obj, form, change):
                if obj.user_to.saldo < obj.amount:
                    raise ValidationError("saldo tidak mencukupi")
                else:
                    obj.save()
                    if obj.transaction_type == 'debit':
                        obj.user_to.saldo -= obj.amount
                    # elif obj.transaction_type == 'transfer':
                    #     obj.user_to.saldo += obj.amount
                    #     obj.user_from.saldo -= obj.amount
                    else:
                        obj.user_to.saldo += obj.amount
                    obj.user_to.save()

class RekeningAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'jenis_rekening', 'nomer_rekening', 'saldo', 'tanggal_join', 'user_id_id')
    readonly_fields = ['nomer_rekening', 'saldo',]

@admin.register(History)
class HistoryAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'saldo_sebelum', 'saldo_sesudah', 'waktu', 'rekening_id', 'transaksi_id')

admin.site.register(Rekening, RekeningAdmin)
admin.site.register(Transaction, TransactionAdmin)
# Register your models here.
