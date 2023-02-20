from siswa.models import Produk
from rest_framework import serializers

class ProdukSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Produk
        fields = ['nama', 'kategori', 'harga']