from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.contrib.auth.models import User, UserManager, Permission, Group
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout, password_validation, hashers
from django.core import exceptions, validators
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from django.conf import settings
from .models import DBorg,DBppw,DBrpt
from django.contrib.auth.hashers import check_password
from django.contrib.contenttypes.models import ContentType

from fpdf import FPDF
from io import BytesIO

from bokeh.palettes import Category20c, Viridis, Spectral
from bokeh.transform import cumsum
from bokeh.plotting import figure, curdoc, output_file, show
from bokeh.embed import components
from bokeh.resources import CDN
from bokeh.models import ColumnDataSource, HoverTool, formatters
import math
import pandas as pd
from datetime import *

def validate_pass(pass1,pass2):  
        if (pass1 and pass2 and pass1 == pass2):
            return True
        else :
            return False

class PDF(FPDF):
    # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', '', 9)
        # Page number
        if self.page_no() != 1:
            self.cell(0, 10, 'Page ' + str(self.page_no()-1), 0, 0, 'C')

listheading = ["1.0 Tujuan", "2.0 Latar Belakang", "3.0 Objektif", "4.0 Anjuran", "5.0 Cadangan Tarikh dan Tempat", "6.0 Penyertaan", "7.0 Jawatankuasa", "8.0 Implikasi Kewangan", "9.0 Kesimpulan"] 

def prosesPDF(kepala,perut, maklumat):
    #satu page h = 255
    pdf = PDF('P', 'mm', 'A4')
    pdf.add_page()
    #tajuk
    pdf.set_font('Arial', 'BU', 16)
    pdf.cell(w=0, h=55, txt=perut[0], border=0, ln=1, align='C', fill=0)
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(w=0, h=130, txt=maklumat[0], border=0, ln=1, align='C', fill=0)
    pdf.cell(w=0, h=15, txt="Disediakan Oleh: ", border=0, ln=1, align='C', fill=0)
    pdf.cell(w=0, h=15, txt=maklumat[1], border=0, ln=1, align='C', fill=0)
    pdf.cell(w=0, h=40, txt="", border=0, ln=1, align='C', fill=0)
    
    #tujuan
    pdf.set_font('Arial', 'B', 15)
    pdf.cell(w=0, h= 13, txt=kepala[0], border=0, ln=1, align='L', fill=0)
    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(w=0, h=5, txt= perut[1], border=0, align='J', fill=0)
    
    #latar belakang
    pdf.set_font('Arial', 'B', 15)
    pdf.cell(w=0, h=13, txt=kepala[1], border=0, ln=1, align='L', fill=0)
    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(w=0, h=5, txt=perut[2], border=0, align='J', fill=0)
    
    #objektif
    pdf.set_font('Arial', 'B', 15)
    pdf.cell(w=0, h=13, txt=kepala[2], border=0, ln=1, align='L', fill=0)
    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(w=0, h=5, txt=perut[3], border=0, align='J', fill=0)
    
    #anjuran
    pdf.set_font('Arial', 'B', 15)
    pdf.cell(w=0, h=13, txt=kepala[3], border=0, ln=1, align='L', fill=0)
    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(w=0, h=5, txt=perut[4], border=0, align='J', fill=0)
    
    #cadangan tarikh
    pdf.set_font('Arial', 'B', 15)
    pdf.cell(w=0, h=13, txt=kepala[4], border=0, ln=1, align='L', fill=0)
    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(w=0, h=5, txt=perut[5], border=0, align='J', fill=0)
    
    #penyertaan
    pdf.set_font('Arial', 'B', 15)
    pdf.cell(w=0, h=13, txt=kepala[5], border=0, ln=1, align='L', fill=0)
    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(w=0, h=5, txt=perut[6], border=0, align='J', fill=0)
    
    #jawatankuasa
    pdf.set_font('Arial', 'B', 15)
    pdf.cell(w=0, h=13, txt=kepala[6], border=0, ln=1, align='L', fill=0)
    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(w=0, h=5, txt=perut[7], border=0, align='J', fill=0)
    
    #iplikasi kewangan
    pdf.set_font('Arial', 'B', 15)
    pdf.cell(w=0, h=13, txt=kepala[7], border=0, ln=1, align='L', fill=0)
    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(w=0, h=5, txt=perut[8], border=0, align='J', fill=0)
    
    #kesimpulan
    pdf.set_font('Arial', 'B', 15)
    pdf.cell(w=0, h=13, txt=kepala[8], border=0, ln=1, align='L', fill=0)
    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(w=0, h=5, txt=perut[9], border=0, align='J', fill=0)
    
    pdf.cell(w=0, h=15, txt="", border=0, ln=1, align='L', fill=0)
    pdf.set_auto_page_break(auto = True, margin = 45)
    
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(w=0, h=5, txt="Disediakan Oleh: ", border=0, ln=1, align='L', fill=0)
    pdf.cell(w=0, h=10, txt="", border=0, ln=1, align='L', fill=0)
    pdf.cell(w=0, h=10, txt="..........................................", border=0, ln=1, align='L', fill=0)
    pdf.cell(w=0, h=5, txt=maklumat[1], border=0, ln=1, align='L', fill=0)
    pdf.set_font('Arial', '', 12)
    pdf.cell(w=0, h=5, txt=maklumat[2], border=0, ln=1, align='L', fill=0)
    pdf.cell(w=0, h=5, txt=maklumat[0], border=0, ln=1, align='L', fill=0)
    
    pdf.cell(w=0, h=15, txt="", border=0, ln=1, align='L', fill=0)
    pdf.set_auto_page_break(auto = True, margin = 75)
    
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(w=0, h=5, txt="Disokong Oleh: ", border=0, ln=1, align='L', fill=0)
    pdf.cell(w=0, h=10, txt="", border=0, ln=1, align='L', fill=0)
    pdf.cell(w=0, h=10, txt="..........................................", border=0, ln=1, align='L', fill=0)
    pdf.cell(w=0, h=5, txt=maklumat[3], border=0, ln=1, align='L', fill=0)
    pdf.set_font('Arial', '', 12)
    pdf.cell(w=0, h=5, txt=maklumat[4], border=0, ln=1, align='L', fill=0)
    pdf.cell(w=0, h=5, txt=maklumat[5], border=0, ln=1, align='L', fill=0)
    
    return pdf.output(dest='S').encode('latin-1')


#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~User and Index Part 
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------

#*************---------------   index   ---------------*************
def index(request):
    return render(request, 'PaperworkManagement/index.html')

def upcoming(request):
    tahun = datetime.now().year
    bulan = datetime.now().month
    hari = datetime.now().day
    
    incomingthismonth = []
    incomingthisyear = []
    incomingnextyear = []
    
    incomingthismonth = DBppw.objects.filter(stats_tarikh__year = tahun, stats_tarikh__month = bulan,stats_tarikh__day__gte = hari,ppwdone = True).order_by('stats_tarikh')
    
    if bulan == 12:
        pass
    elif bulan<12 and bulan>0:
        incomingthisyear = DBppw.objects.filter(stats_tarikh__year = tahun, stats_tarikh__month__gte = bulan+1,ppwdone = True).order_by('stats_tarikh')
        
    incomingnextyear = DBppw.objects.filter(stats_tarikh__year__gte = tahun+1, ppwdone = True).order_by('stats_tarikh')
    
    all_incoming_ppw = list(incomingthismonth) + list(incomingthisyear) + list(incomingnextyear)
    
    context = {
        'allppw_list' : all_incoming_ppw[:10]
        }
    
    return render(request, 'PaperworkManagement/upcoming_event.html',context)

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~End of User and Index Part 
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------



#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Authentication Part 
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------

#*************---------------   login   ---------------*************
def login(request):
    return render(request,'PaperworkManagement/login.html')

#check login
def auth_user(request):
    username = request.POST['username']
    password = request.POST['password']
    
    user = authenticate(request, username = username, password = password)
    
    if user is not None:
        auth_login(request,user)
        try:
            return view_ppw(request)
        except:
            return render(request, 'PaperworkManagement/index.html', {'success' : "You successfully login"})
    else:
        return render(request,'PaperworkManagement/login.html', {'error_message' : "Your password or username is invalid.",})



#*************---------------   signup   ---------------*************
def signup(request):
    return render(request, 'PaperworkManagement/signup.html')

#check user signup
def signup_process(request):
    '''
    To validate sign up information
    '''
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']
    repassword = request.POST['repassword']
    
    try:
        password_validation.validate_password( password, username, None)
        
    except password_validation.ValidationError as error:
        return render(request, 'PaperworkManagement/signup.html', {'error_message' : error,})
    
    if User.objects.filter(username = username).exists():
        return render(request, 'PaperworkManagement/signup.html', {'error_message' : "That username had already been taken.",})
    else:
        if (validate_pass(password,repassword)):
            user = User.objects.create_user(username = username, email = email, password = password)
                
            group = Group.objects.get(name = 'ppwuser')
            user.groups.add(group)
                
            user.save()
            return render(request, 'PaperworkManagement/index.html', {'success' : "You successfully sign up.",})
        else:
            return render(request, 'PaperworkManagement/signup.html', {'error_message' : "Your password did not match.",})



#*************---------------   admin signup   ---------------*************
def signup_admin(request):
    return render(request, 'PaperworkManagement/signup_admin.html')

def process_admin(request):
    '''
    To validate sign up information
    '''
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']
    repassword = request.POST['repassword']
    orgcode = request.POST['orgcode']
    orgpass = request.POST['orgpass']
    
    org = get_object_or_404(DBorg, pk = orgcode)
    try:
        password_validation.validate_password( password, username, None)
        
    except password_validation.ValidationError as error:
        return render(request, 'PaperworkManagement/signup_admin.html', {'error_message' : error,})
    
    if check_password(orgpass,org.orgpass): #check organization password
        if not User.objects.filter(username = username).exists(): #check username exist
            if (validate_pass(password,repassword)): #validate password
                user = User.objects.create_user(username = username, email = email, password = password) #create user
                
                if Group.objects.filter(name = 'ppwadmin_' + orgcode).exists(): #check group exist or not
                
                    group = Group.objects.get(name = 'ppwadmin_' + orgcode)
                    user.groups.add(group)
                    
                    user.save()
        
                else:
                    newgroup = Group.objects.create(name = 'ppwadmin_' + orgcode) #create new group
                    
                    permgroup = Permission.objects.get(codename = 'change_dbppw')#create permission
                    newgroup.permissions.add(permgroup)
                    
                    user.groups.add(newgroup)
                    
                    user.save()
                
                return render(request, 'PaperworkManagement/index.html', {'success' : "You successfully sign up as admin at " + org.orgname,})
            else:
                return render(request, 'PaperworkManagement/signup_admin.html', {'error_message' : "Your password did not match.",})
        else:
            return render(request, 'PaperworkManagement/signup_admin.html', {'error_message' : "That username had already been taken.",})
    else:
        return render(request, 'PaperworkManagement/signup_admin.html', {'error_message' : "Your organization name or password did not match.",})
    
    
#*************---------------   organization signup   ---------------*************
def signup_org(request):
    return render(request, 'PaperworkManagement/signup_org.html')

def process_org(request):
    '''
    To validate sign up information
    '''
    orgname = request.POST['orgname']
    orgcode = request.POST['orgcode']
    orgpass = request.POST['orgpassword']
    orgrepass = request.POST['orgrepassword']
    
    try:
        password_validation.validate_password( orgpass, orgcode, None)
        
    except password_validation.ValidationError as error:
        return render(request, 'PaperworkManagement/signup_org.html', {'error_message' : error,})
            
    if DBorg.objects.filter(orgcode = orgcode).exists():
        return render(request, 'PaperworkManagement/signup_org.html', {'error_message' : "That codename had already been taken.",})
    else:
        if (validate_pass(orgpass,orgrepass)):
            encryptpass = hashers.make_password(orgpass)
            neworg = DBorg.objects.create(orgname = orgname, orgcode = orgcode, orgpass = encryptpass)
            
            neworg.save()
            return render(request, 'PaperworkManagement/index.html', {'success' : "Organization registered successfully.",})
        else:
            return render(request, 'PaperworkManagement/signup_org.html', {'error_message' : "Your password did not match.",})



#*************---------------   logout   ---------------*************
def logout(request):
    auth_logout(request)
    return render(request, 'PaperworkManagement/index.html')

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~End of Authentication Part
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------





#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Paperwork Part
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def view_ppw(request):
    name = str(request.user.groups.all()[0])
    orgcode = name[9:]
    org = get_object_or_404(DBorg, pk = orgcode)
    doneppw = DBppw.objects.filter(org = orgcode, ppwdone = True, penulisppw = request.user.email).order_by('-tarikhppw')
    undoneppw = DBppw.objects.filter(org = orgcode, ppwdone = False, penulisppw = request.user.email).order_by('-tarikhppw')
    context = {
        'done_ppw_list' : doneppw,
        'undone_ppw_list' : undoneppw
        }
    return render(request, 'PaperworkManagement/view_ppw.html', context)
    
#*************---------------   write paperwork   ---------------*************
def write_ppw(request):
    return render(request, 'PaperworkManagement/write_ppw.html')

#*************---------------   process paperwork   ---------------*************
def process_ppw(request):
    
    #find organization
    name = str(request.user.groups.all()[0])
    orgcode = name[9:]
    org = get_object_or_404(DBorg, pk = orgcode)
    
    user = get_object_or_404(User, username = request.user.username)
    if not user.first_name and not user.last_name:
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        user.first_name = firstname
        user.last_name = lastname
        user.save()
    
    #data from web
    web_tajukppw = request.POST['tajukppw']
    web_penulisppw = request.user.email
    
    web_tujuan= request.POST['tujuan']
    web_latar = request.POST['latar']
    web_obj = request.POST['obj']
    web_anjuran = request.POST['anjuran']
    web_cadangantarikh = request.POST['cadangantarikh']
    web_penyertaan = request.POST['penyertaan']
    web_ajk = request.POST['ajk']
    web_impkewangan = request.POST['impkewangan']
    web_kesimpulan = request.POST['kesimpulan']
    
    web_stats_peserta = request.POST['ppwpeserta']
    web_stats_budgets = request.POST['ppwbudget']
    web_stats_budgets_makanan = request.POST['ppwbudget_makanan']
    web_stats_budgets_pengangkutan = request.POST['ppwbudget_pengangkutan']
    web_stats_budgets_penginapan = request.POST['ppwbudget_penginapan']
    web_stats_budgets_hadiah = request.POST['ppwbudget_hadiah']
    web_stats_tarikh = request.POST['ppwtarikh']
    
    web_jawatan = request.POST['jawatansaya']
    web_namasokong = request.POST['namasokong']
    web_jawatansokong = request.POST['jawatansokong']
    web_lokasisokong = request.POST['lokasisokong']
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #declare data
    tajukppw = " "
    
    tujuan = " "
    latar = " "
    obj = " "
    anjuran = " "
    cadangantarikh = " "
    penyertaan = " "
    ajk = " "
    impkewangan = " "
    kesimpulan = " "
    
    stats_peserta = 0.00
    stats_budgets = 0.00
    stats_budgets_makanan = 0.00
    stats_budgets_pengangkutan = 0.00
    stats_budgets_penginapan = 0.00
    stats_budgets_hadiah = 0.00
    stats_tarikh = now
    
    jawatan = " "
    namasokong = " "
    jawatansokong = " "
    lokasisokong = " "
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #rewrite data
    try:
        tajukppw = web_tajukppw
    except:
        pass
    
    try:
        tujuan = web_tujuan
    except:
        pass
        
    try:
        latar = web_latar
    except:
        pass
    
    try:
        obj = web_obj
    except:
        pass
    
    try:
        anjuran = web_anjuran
    except:
        pass
    
    try:
        cadangantarikh = web_cadangantarikh
    except:
        pass
    
    try:
        penyertaan = web_penyertaan
    except:
        pass
    
    try:
        ajk = web_ajk
    except:
        pass
    
    try:
        impkewangan = web_impkewangan
    except:
        pass
    
    try:
        kesimpulan = web_kesimpulan
    except:
        pass
    
    listcontent = [tajukppw, tujuan, latar, obj, anjuran, cadangantarikh, penyertaan, ajk, impkewangan, kesimpulan] # list content
    
    try:
        jawatan = web_jawatan
    except:
        pass
    
    try:
        namasokong = web_namasokong
    except:
        pass
    
    try:
        jawatansokong = web_jawatansokong
    except:
        pass
    
    try:
        lokasisokong = web_lokasisokong
    except:
        pass
    
    
    #~~~~~~~~~~~statistical part
    
    #stats jumlah peserta
    try:
        stats_peserta = float(web_stats_peserta)
    except:
        pass
    
    #stats jumlah budget
    try:
        stats_budgets = float(web_stats_budgets)
    except:
        pass
        
    #stats budget untuk makanan
    try:
        stats_budgets_makanan = float(web_stats_budgets_makanan)
    except:
        pass
        
    #stats budget untuk pengangkutan
    try:
        stats_budgets_pengangkutan = float(web_stats_budgets_pengangkutan)
    except:
        pass
        
    #stats budget untuk penginapan
    try:
        stats_budgets_penginapan = float(web_stats_budgets_penginapan)
    except:
        pass
    
    #stats budget untuk hadiah
    try:
        stats_budgets_hadiah = float(web_stats_budgets_hadiah)
    except: 
        pass
    
    #tarikh program dijalankan
    try:
        stats_tarikh = web_stats_tarikh
    except: 
        pass
        
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
     
    listmaklumat = [org.orgname, request.user.get_full_name(), jawatan, namasokong, jawatansokong, lokasisokong]
    
    #save dalam database
    code = request.POST['ppwcode']
    ppwcode = orgcode + '_' + code
    
    if "Process" in request.POST:
        if DBppw.objects.filter(ppwcode = ppwcode).exists():
            return render(request, 'PaperworkManagement/write_ppw.html', {'code_error_message' : "The paperwork code had already be in use",})
        
        newppw = DBppw.objects.create(ppwcode = ppwcode, tajukppw = tajukppw, penulisppw = web_penulisppw, #3
                                      tujuan = tujuan, latar = latar, objektif = obj, anjuran = anjuran, cadangantarikh = cadangantarikh, #5
                                      penyertaan = penyertaan,ajk = ajk, impkewangan = impkewangan, kesimpulan = kesimpulan, #4
                                      stats_peserta = stats_peserta, #1
                                      stats_budgets = stats_budgets, stats_budgets_makan = stats_budgets_makanan,#2
                                      stats_budgets_transport = stats_budgets_pengangkutan, stats_budgets_penginapan = stats_budgets_penginapan, #2
                                      stats_budgets_hadiah = stats_budgets_hadiah,stats_tarikh = stats_tarikh, #3
                                      org = org, #1
                                      jawatanpenulis = web_jawatan, #1
                                      namasokong = namasokong, jawatansokong = jawatansokong,#2
                                      lokasisokong = lokasisokong, ppwdone = True) #1
        newppw.save()
        
        jumlahb = 0
        jumlahp = 0
        
        for ppw in ppw_list:
            jumlahb += ppw.stats_budgets
            jumlahp += ppw.stats_peserta
                
        org.stats_jumlah_budgets = jumlahb
        org.stats_jumlah_peserta = jumlahp
        org.save()
    
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #buat pdf
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename= '+ tajukppw + '.pdf'
    
        buat_pdf= prosesPDF(listheading, listcontent, listmaklumat)
        response.write(buat_pdf) 
        
        return response
    
    elif "Save" in request.POST:
        if DBppw.objects.filter(ppwcode = ppwcode).exists():
            ppwexist = get_object_or_404(DBppw, ppwcode = ppwcode)
            
            ppwexist.ppwcode = ppwcode
            ppwexist.tajukppw = tajukppw
            ppwexist.penulisppw = web_penulisppw
            ppwexist.tujuan = tujuan
            ppwexist.latar = latar
            ppwexist.objektif = obj
            ppwexist.anjuran = anjuran 
            ppwexist.cadangantarikh = cadangantarikh
            ppwexist.penyertaan = penyertaan
            ppwexist.ajk = ajk
            ppwexist.impkewangan = impkewangan
            ppwexist.kesimpulan = kesimpulan
            ppwexist.stats_peserta = stats_peserta
            ppwexist.stats_budgets = stats_budgets
            ppwexist.stats_budgets_makan = stats_budgets_makanan
            ppwexist.stats_budgets_transport = stats_budgets_pengangkutan
            ppwexist.stats_budgets_penginapan = stats_budgets_penginapan
            ppwexist.stats_budgets_hadiah = stats_budgets_hadiah
            ppwexist.stats_tarikh = stats_tarikh
            ppwexist.org = org
            ppwexist.jawatanpenulis = web_jawatan
            ppwexist.namasokong = namasokong
            ppwexist.jawatansokong = jawatansokong
            ppwexist.lokasisokong = lokasisokong
            ppwexist.ppwdone = False
            
            ppwexist.save()
        
        else:
            newppw = DBppw.objects.create(ppwcode = ppwcode, tajukppw = tajukppw, penulisppw = web_penulisppw, #3
                                      tujuan = tujuan, latar = latar, objektif = obj, anjuran = anjuran, cadangantarikh = cadangantarikh, #5
                                      penyertaan = penyertaan,ajk = ajk, impkewangan = impkewangan, kesimpulan = kesimpulan, #4
                                      stats_peserta = stats_peserta, #1
                                      stats_budgets = stats_budgets, stats_budgets_makan = stats_budgets_makanan,#2
                                      stats_budgets_transport = stats_budgets_pengangkutan, stats_budgets_penginapan = stats_budgets_penginapan, #2
                                      stats_budgets_hadiah = stats_budgets_hadiah,stats_tarikh = stats_tarikh, #3
                                      org = org, #1
                                      jawatanpenulis = web_jawatan, #1
                                      namasokong = namasokong, jawatansokong = jawatansokong,#2
                                      lokasisokong = lokasisokong, ppwdone = False) #1
            newppw.save()
        return view_ppw(request)
    
    elif 'Edit' in request.POST:
        try:
            ppwexist = get_object_or_404(DBppw, ppwcode = ppwcode)
            
            ppwexist.ppwcode = ppwcode
            ppwexist.tajukppw = tajukppw
            ppwexist.penulisppw = web_penulisppw
            ppwexist.tujuan = tujuan
            ppwexist.latar = latar
            ppwexist.objektif = obj
            ppwexist.anjuran = anjuran 
            ppwexist.cadangantarikh = cadangantarikh
            ppwexist.penyertaan = penyertaan
            ppwexist.ajk = ajk
            ppwexist.impkewangan = impkewangan
            ppwexist.kesimpulan = kesimpulan
            ppwexist.stats_peserta = stats_peserta
            ppwexist.stats_budgets = stats_budgets
            ppwexist.stats_budgets_makan = stats_budgets_makanan
            ppwexist.stats_budgets_transport = stats_budgets_pengangkutan
            ppwexist.stats_budgets_penginapan = stats_budgets_penginapan
            ppwexist.stats_budgets_hadiah = stats_budgets_hadiah
            ppwexist.stats_tarikh = stats_tarikh
            ppwexist.org = org
            ppwexist.jawatanpenulis = web_jawatan
            ppwexist.namasokong = namasokong
            ppwexist.jawatansokong = jawatansokong
            ppwexist.lokasisokong = lokasisokong
            ppwexist.ppwdone = True
            
            ppwexist.save()
            
            name = str(request.user.groups.all()[0])
            orgcode = name[9:]
            org = get_object_or_404(DBorg, pk = orgcode)
            ppw_list = DBppw.objects.filter(org = orgcode).order_by('-tarikhppw')
            
            jumlahb = 0
            jumlahp = 0
            
            for ppw in ppw_list:
                jumlahb += ppw.stats_budgets
                jumlahp += ppw.stats_peserta
                
            org.stats_jumlah_budgets = jumlahb
            org.stats_jumlah_peserta = jumlahp
            org.save()
            
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename= '+ tajukppw + '.pdf'
        
            buat_pdf= prosesPDF(listheading, listcontent, listmaklumat)
            response.write(buat_pdf) 
            
            return response
        
        except:
            return update_ppw(request, ppwcode)

def update_ppw(request, ppwcode):
    name = str(request.user.groups.all()[0])
    orgcode = name[9:]
    org = get_object_or_404(DBorg, pk = orgcode)
    filtering= len(str(orgcode)) + 1
    
    try:
        ppw = get_object_or_404(DBppw,ppwcode = ppwcode)
        context = {
            'ppwcode' : ppw.ppwcode[filtering:],
            'tajuk' : ppw.tajukppw,
            'tujuan' : ppw.tujuan,
            'latar' : ppw.latar,
            'obj' : ppw.objektif,
            'anjuran' : ppw.anjuran,
            'tarikh' : ppw.cadangantarikh,
            'ppwtarikh' : ppw.stats_tarikh,
            'peserta' : ppw.penyertaan,
            'bilpeserta' : ppw.stats_peserta,
            'ajk' : ppw.ajk,
            'impwang' : ppw.impkewangan,
            'bajet' : ppw.stats_budgets,
            'bajetmakanan' : ppw.stats_budgets_makan,
            'bajetpengangkutan' : ppw.stats_budgets_transport,
            'bajetpenginapan' : ppw.stats_budgets_penginapan,
            'bajethadiah' : ppw.stats_budgets_hadiah,
            'kesimpulan' : ppw.kesimpulan,
            'jawatan' : ppw.jawatanpenulis,
            'namasokong' : ppw.namasokong,
            'jawatansokong' : ppw.jawatansokong,
            'lokasisokong' : ppw.lokasisokong,
            }
        
        return render(request, 'PaperworkManagement/write_ppw.html', context)
    except:
        return render(request, 'PaperworkManagement/write_ppw.html', { 'code_error_message' : "There are error processing paperwork, did you change the paperwork code?"})
        

def delete_ppw(request, ppwcode):
    name = str(request.user.groups.all()[0])
    orgcode = name[9:]
    org = get_object_or_404(DBorg, pk = orgcode)
    ppw = get_object_or_404(DBppw, ppwcode = ppwcode)
    ppw_list = DBppw.objects.filter(org = orgcode, ppwdone = True).order_by('-tarikhppw')
    
    ppw.delete()
    
    jumlahb = 0
    jumlahp = 0
        
    for ppw in ppw_list:
        jumlahb += ppw.stats_budgets
        jumlahp += ppw.stats_peserta
            
    org.stats_jumlah_budgets = jumlahb
    org.stats_jumlah_peserta = jumlahp
    org.save()
    return view_ppw(request)

def done_ppw(request):
    if 'Done' in request.POST:
        return view_ppw(request)
    elif 'Back' in request.POST:
        return view_ppw(request)

#*************---------------   load saved paperwork   ---------------*************

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~End of Paperwork Part
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------




#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Organization Part
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#*************---------------   organization dashboard   ---------------*************
def view_org(request):
    
    #find organization
    name = str(request.user.groups.all()[0])
    orgcode = name[9:]
    org = get_object_or_404(DBorg, pk = orgcode)
    ppw = DBppw.objects.filter(org = orgcode, ppwdone = True).order_by('-tarikhppw')
    context = {
        'ppw_list' : ppw
        }
    return render(request, 'PaperworkManagement/org_view.html', context)

def dlppw(request, ppwcode):
    
    #get paperwork
    ppw = get_object_or_404(DBppw, ppwcode = ppwcode)
    #get writer
    penulis = get_object_or_404(User,email = ppw.penulisppw)
    #get organization
    name = str(request.user.groups.all()[0])
    orgcode = name[9:]
    org = get_object_or_404(DBorg, pk = orgcode)
    
    listcontent = [ppw.tajukppw, ppw.tujuan, ppw.latar, ppw.objektif, ppw.anjuran, ppw.cadangantarikh, ppw.penyertaan, ppw.ajk, ppw.impkewangan, ppw.kesimpulan]
    
    listmaklumat = [org.orgname, penulis.get_full_name(), ppw.jawatanpenulis, ppw.namasokong, ppw.jawatansokong, ppw.lokasisokong]
    
    #buat pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename= '+ ppw.tajukppw + '.pdf'

    buat_pdf= prosesPDF(listheading, listcontent, listmaklumat)
    response.write(buat_pdf) 
    
    return response

def budget_flow(request):
    
    name = str(request.user.groups.all()[0])
    orgcode = name[9:]
    org = get_object_or_404(DBorg, pk = orgcode)
    ppw_list = DBppw.objects.filter(org = orgcode, ppwdone = True).order_by('-tarikhppw')
    ppw_list10 = DBppw.objects.filter(org = orgcode, ppwdone = True).order_by('-tarikhppw')[:10]
    filtering = len(str(orgcode)) + 1
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #-------------------------------bar graph budget per program-----------------
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    program = []
    bajet = []
    
    for ppw in ppw_list10:
        
        program.append(ppw.ppwcode[filtering:])
        bajet.append(ppw.stats_budgets)

    source = ColumnDataSource(data=dict(program=program, bajet=bajet))

    bar = figure(x_range=program, plot_width =1000, plot_height=500, title="Budgets per Program (10 latest program)", toolbar_location="right", tools="hover,save")
    
    hover = bar.select(dict(type=HoverTool))
    hover.tooltips = [
    ("Program", "@program"),
    ("Budget", "@bajet{1.11}"),
    ]

    bar.vbar(x='program', top='bajet', width=0.9, source = source, line_color = 'white')

    bar.xgrid.grid_line_color = None
    bar.y_range.start = 0

    script, div = components(bar,CDN)
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #-------------------------------pie chart budget proportion -----------------
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    bajetmakanan  = 0.00
    rmakanan = 0
    bajettransport = 0.00
    rtransport = 0
    bajetpenginapan = 0.00
    rpenginapan = 0
    bajethadiah = 0.00
    rhadiah = 0
    
    for ppw in ppw_list:
        
        if ppw.stats_budgets_makan > 0.00:
            bajetmakanan += ppw.stats_budgets_makan
            rmakanan += 1
            
        if ppw.stats_budgets_transport > 0.00:
            bajettransport += ppw.stats_budgets_transport
            rtransport += 1
            
        if ppw.stats_budgets_penginapan > 0.00:
            bajetpenginapan += ppw.stats_budgets_penginapan
            rpenginapan += 1
            
        if ppw.stats_budgets_hadiah > 0.00:
            bajethadiah += ppw.stats_budgets_hadiah
            rhadiah += 1

    x = {
    'Food Budget': bajetmakanan,
    'Transportation Budget': bajettransport,
    'Accommodation Budget': bajetpenginapan,
    'Prize Budget': bajethadiah
    }

    data = pd.Series(x).reset_index(name='bajet').rename(columns={'index':'pecahan'})
    data['angle'] = data['bajet']/data['bajet'].sum() * 2*math.pi
    #data['color'] = Category20c[len(x)]
    #data['color'] = Viridis[len(x)]
    data['color'] = Spectral[len(x)]
    
    p = figure(plot_height=559,plot_width=1000, title="Budget Proportion", toolbar_location="right",
               tools="hover, save", x_range=(-0.5, 1.0))
    
    p.wedge(x=0, y=1, radius=0.4,
            start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
            line_color="white", fill_color='color', legend='pecahan', source=data)
    
    p.axis.axis_label=None
    p.axis.visible=False
    p.grid.grid_line_color = None
    
    hover = p.select(dict(type=HoverTool))
    hover.tooltips = [
    ("Proportion", "@pecahan"),
    ("Budget", "@bajet{1.11}"),
    ]


    script2, div2 = components(p, CDN)
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #-------------------------------bar graph program per month-----------------
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    monthprogram = []
    month = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    jan = 0
    feb = 0
    march = 0
    april = 0
    may = 0
    june = 0
    july = 0
    aug = 0
    sep = 0
    oct = 0
    nov = 0
    dec = 0
    
    tahun = datetime.now().year #get current year
    
    for bulan in range(1,13):
        
        ppwbulan = DBppw.objects.filter(org = orgcode, stats_tarikh__month=bulan,stats_tarikh__year = tahun, ppwdone = True)
        monthprogram.append(len(ppwbulan))

    source = ColumnDataSource(data=dict(month=month, monthprogram=monthprogram))

    bar = figure(x_range=month, plot_width =1000, plot_height=500, title="Program per Month in " + str(tahun), toolbar_location="right", tools="hover,save")
    
    hover = bar.select(dict(type=HoverTool))
    hover.tooltips = [
    ("Month", "@month"),
    ("Program Amount", "@monthprogram{1}"),
    ]

    bar.vbar(x='month', top='monthprogram', width=0.9, source = source, line_color = 'white')

    bar.xgrid.grid_line_color = None
    bar.y_range.start = 0

    script3, div3 = components(bar,CDN)
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    total = org.stats_jumlah_budgets
    
    avgmakan = 0.00
    avgtransport = 0.00
    avgpenginapan = 0.00
    avghadiah = 0.00
    
    try:
        avgmakan = bajetmakanan/rmakanan
        avgtransport = bajettransport/rtransport
        avgpenginapan = bajetpenginapan/rpenginapan
        avghadiah = bajethadiah/rhadiah
    except:
        pass
    
    kira = [avgmakan,avgtransport,avgpenginapan,avghadiah]
    jawapan = ["Food", "Transport", "Accomodation", "Prize"]
    highest = kira[0]
    highestjawapan = 0
    lowest = kira[0]
    lowestjawapan = 0
    
    for i in range(0,len(kira)):
        
        if kira[i] > highest:
            highest = kira[i]
            highestjawapan = i
            
        elif kira[i] < lowest:
            lowest = kira[i]
            lowestjawapan = i
    
    if highest <= 0:
        jawapan[highestjawapan] = "Not enough data"
        
    if lowest <= 0:
        jawapan[lowestjawapan] = "Not enough data"
        
    return render(request, "PaperworkManagement/budget_flow.html", {"the_script":script, "the_div":div,
                                                                    "the_script2":script2, "the_div2":div2,
                                                                    "the_script3":script3, "the_div3":div3,
                                                                    "total" : total, "aktiviti" :len(ppw_list),
                                                                    "bilmakan" : rmakanan, "avgmakan" : avgmakan,
                                                                    "biltransport" : rtransport, "avgtransport" : avgtransport,
                                                                    "bilpenginapan" : rpenginapan, "avgpenginapan" : avgpenginapan,
                                                                    "bilhadiah" : rhadiah, "avghadiah" : avghadiah,
                                                                    "highest" : jawapan[highestjawapan], "lowest" : jawapan[lowestjawapan]})

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~End of Organization Part
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------