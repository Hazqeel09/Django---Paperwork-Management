from django.db import models
from django_mysql import models as dm

from django.utils.timezone import now
from django.contrib.auth.models import User

# Create your models here.

class DBorg(models.Model):
    orgname = models.TextField()
    orgcode = models.CharField(max_length = 159, default = "orgcode98", primary_key = True)
    orgpass = models.CharField(max_length = 159, default = "orgpass98")
    
    stats_jumlah_peserta = models.IntegerField(default = 0)
    stats_jumlah_budgets = models.FloatField(default = 0)
    
    def __str__(self):
        return self.orgname

class DBppw(models.Model):
    ppwcode = models.CharField(max_length = 159, primary_key = True)
    tajukppw = models.TextField()
    penulisppw = models.EmailField()
    tarikhppw = models.DateTimeField(default = now)#bila paperwork ditulis?
    
    tujuan = models.TextField() #1
    latar = models.TextField() #2
    objektif = models.TextField() #3
    anjuran = models.TextField() #4
    cadangantarikh = models.TextField() #5
    penyertaan = models.TextField() #6
    ajk = models.TextField() #7
    impkewangan = models.TextField() #8
    kesimpulan = models.TextField() #9
    
    ppwdone = models.BooleanField(default = False)
    
    stats_peserta = models.IntegerField(default = 0)
    stats_budgets = models.FloatField(default = 0)
    stats_budgets_makan = models.FloatField(default = 0)
    stats_budgets_transport = models.FloatField(default = 0)
    stats_budgets_penginapan = models.FloatField(default = 0)
    stats_budgets_hadiah = models.FloatField(default = 0)
    stats_tarikh = models.DateField(default = now) #bila buat event?
    
    jawatanpenulis = models.CharField(max_length = 159, default = "Jawatan")
    namasokong = models.CharField(max_length = 159, default = "Nama")
    jawatansokong = models.CharField(max_length = 159, default = "Jawatan")
    lokasisokong = models.CharField(max_length = 159, default = "Lokasi")
    
    
    org = models.ForeignKey(DBorg, on_delete= models.CASCADE)
    
    def __str__(self):
        return self.tajukppw

    
class DBrpt(models.Model):
    ppwcode = models.ForeignKey(DBppw, on_delete = models.CASCADE)
    rptcode = models.CharField(max_length = 159, primary_key = True)
    tajukrpt = models.TextField()
    penulisrpt = models.EmailField()
    tarikhrpt = models.DateTimeField(default = now)
    
    org = models.ForeignKey(DBorg, on_delete= models.CASCADE)
    
    share_to_public = models.BooleanField(default = True)
    
    def __str__(self):
        return self.tajukrpt
    
    
