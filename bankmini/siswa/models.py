from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.utils.timezone import now
from django.db.models.signals import post_save
from django.dispatch import receiver
import random

# Create your models here.
class ProfileUser(models.Model):
    alamat = models.CharField(max_length=244)
    tanggal_lahir = models.DateField()
    profile = models.ImageField(upload_to='media/%Y/%m/%d/', null=True, default=False)
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user_id)

class Rekening(models.Model):
    JENIS_REKENING = [
        ('tabungan', 'Tabungan'),
        ('giro', 'Giro'),
    ]
    jenis_rekening = models.CharField(choices=JENIS_REKENING, max_length=12)
    nomer_rekening = models.CharField(unique=True, max_length=7)
    saldo = models.FloatField(null=True)
    tanggal_join = models.DateField(auto_now_add=True)
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return '{} - {}'.format(self.nomer_rekening, self.user_id)
    
    def save(self, *args, **kwargs):
        self.nomer_rekening = random.randint(1000000, 9999999)
        super(Rekening, self).save(*args, **kwargs)

    def total_transaction(self):
        return self.transaction_set.count()
    
class Transaction(models.Model):
    user_from = models.ForeignKey(Rekening, related_name='transactions_from', on_delete=models.CASCADE)
    user_to = models.ForeignKey(Rekening, related_name='transactions_to', on_delete=models.CASCADE)
    TRANSACTION_TYPE = [
        ('credit', 'Credit'),
        ('debit', 'Debit'),
        ('transfer', 'Transfer'),
    ]
    transaction_type = models.CharField(choices=TRANSACTION_TYPE, max_length=9, default='transfer')
    amount = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)
        # return '{} to {} - {}'.format(self.id, self.user_from.user_id, self.user_to.user_id, self.amount)
    
class History(models.Model):
    rekening = models.ForeignKey(Rekening, on_delete=models.CASCADE)
    transaksi = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    saldo_sebelum = models.FloatField()
    saldo_sesudah = models.FloatField()
    waktu = models.DateTimeField(auto_now_add=True)


@receiver(post_save, sender=Transaction)
def tambah_history(sender, created, instance, **kwargs):
   if created:
        user_from = instance.user_from
        user_to = instance.user_to
        saldo_sebelum = user_from.saldo
        saldo_sebelums = user_to.saldo
        if instance.transaction_type == 'debit':
            user_from.saldo -= instance.amount
        elif instance.transaction_type == 'transfer':
            user_from.saldo -= instance.amount
            user_to.saldo += instance.amount
        else:
            user_from.saldo += instance.amount
        user_from.save()
        
        
        if instance.transaction_type == 'debit':
            history = History.objects.create(
            rekening=user_from,
            transaksi=instance,
            saldo_sebelum=saldo_sebelum,
            saldo_sesudah=user_from.saldo,
            )
        elif instance.transaction_type == 'credit':
            history = History.objects.create(
            rekening=user_from,
            transaksi=instance,
            saldo_sebelum=saldo_sebelum,
            saldo_sesudah=user_from.saldo,
            )
        else:
            history = History.objects.create(
            rekening=user_from,
            transaksi=instance,
            saldo_sebelum=saldo_sebelum,
            saldo_sesudah=user_from.saldo,
            )

            historys = History.objects.create(
                rekening=user_to,
                transaksi=instance,
                saldo_sebelum=saldo_sebelums,
                saldo_sesudah=user_to.saldo,
            )

        # if instance.transaction_type == 'debit':
        #     history.save()
        # elif instance.transaction_type == 'transfer':
        #     history.save()
        #     historys.save()

#produk
class Produk(models.Model):
    KATEGORI_CHOICES = [
        ('makanan', 'Makanan'),
        ('minuman', 'Minuman'),
    ]
    nama = models.CharField(max_length=244)
    kategori = models.CharField(choices=KATEGORI_CHOICES, default='makanan', max_length=12)
    harga = models.FloatField()

    def __str__(self):
        return self.nama, self.kategori












  