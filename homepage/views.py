from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import HttpResponse
from django.http import FileResponse  

import homepage.models
import homepage.forms
import os
from django.contrib.auth.decorators import login_required 


#爬虫
import requests
from bs4 import BeautifulSoup
import re

#分页
from django.core.paginator import Paginator

def index(request):
    from django.core.paginator import Paginator
	#网站的主页
    fwl=homepage.models.siteinfo.objects.get(id=1)
    fwl.fangwenliang=fwl.fangwenliang+1
    fwl.save()
   # books=homepage.models.Bookinfo.objects.all()
    books=homepage.models.Bookinfo.objects.order_by('length')
    
    xinxi= request.META['HTTP_USER_AGENT']
    aaa = 60
    if("Android" in xinxi):
        aaa= 14
    if("iPhone" in xinxi):
        aaa= 14
    #print(request.META['HTTP_USER_AGENT'])   浏览器信息
    
    
    paginator = Paginator(books, aaa)
        #从前端获取当前的页码数,默认为1
    page = request.GET.get('page',1)
    
    #把当前的页码数转换成整数类型
    currentPage=int(page)

    try:
        #print(page)
        books = paginator.page(page)#获取当前页码的记录
    except PageNotAnInteger:
        books = paginator.page(1)#如果用户输入的页码不是整数时,显示第1页的内容
    except EmptyPage:
        books = paginator.page(paginator.num_pages)#如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
   
    context={'books':books}
    return render(request,'index.html',context)
  
def book(request,book_id):
    book = homepage.models.Bookinfo.objects.get(id=book_id)
    context={'book':book}
    return render(request,'book.html',context)

def writer(request,writer_id):
    writera = homepage.models.Writer.objects.get(id=writer_id)
    books = homepage.models.Bookinfo.objects.filter(writer=writera)
    context={'books':books,'writer':writera}
    return render(request,'writer.html',context)
    
@login_required     
def newbook(request):
    if request.method != 'POST':
        #未提交数据，创建一个新表单
        form = homepage.forms.BookForm()
    else:
        #POST提交的数据，对数据进行处理
        form =homepage.forms.BookForm(request.POST)
        obj = request.FILES.get('fafafa')

        if form.is_valid() and obj!=None:
            if obj.size >828563:
                obj = None
                return HttpResponseRedirect(reverse('index'))
 
            if obj.name[-4:]!='.txt':
                obj = None
                return HttpResponseRedirect(reverse('index'))
            
            newbook= form.save(commit=False)
            newbook.downurl=os.path.join('xz/',obj.name.replace(' ',''))
            newbook.owner = request.user
            newbook.length=len(request.POST['name'])
            newbook.save()
 
         
            f = open(os.path.join('xz/',obj.name.replace(' ','')),'wb+')  
            for line in obj.chunks():
                f.write(line)
            f.close()
        
            return HttpResponseRedirect(reverse('index'))
        else :
            return HttpResponseRedirect(reverse('index'))
    context ={'form':form}
    return render(request,'newbook.html',context)
    
@login_required 
def newwriter(request):
    writers=homepage.models.Writer.objects.all()
    if request.method != 'POST':
        #未提交数据，创建一个新表单
        form =homepage.forms. WriterForm()
    else:
        #POST提交的数据，对数据进行处理
        form =homepage.forms.WriterForm(request.POST)
        if form.is_valid():
            new_writer= form.save(commit=False)

            new_writer.owner = request.user
            new_writer.save()
            return HttpResponseRedirect(reverse('newwriter'))
    context ={'form':form,'writers':writers}
    return render(request,'newwriter.html',context)
    
@login_required 
def file_down(request,book_name):  
    #统计下载量
    a=homepage.models.Bookinfo.objects.get(downurl='xz/'+book_name)
    a.xzl = a.xzl +1
    a.save()
    
    file=open('/root/down/xz/'+book_name,'rb')  
    response =FileResponse(file)  
    response['Content-Type']='application/octet-stream'  
    response['Content-Disposition']='attachment;filename="%s"'  % 'down.txt'
    return response  
    
    
    
def video(request,video_name):  
    print(video_name)
    r = requests.get(url="http://"+video_name)
    print("ok")
    soupp = BeautifulSoup(r.text, "html.parser")
    print("ok")

    return HttpResponse(soupp)

def newliuyan(request):
    liuyans=homepage.models.Liuyan.objects.all()
    if request.method != 'POST':
        #未提交数据，创建一个新表单
        form =homepage.forms. LiuyanForm()
    else:
        #POST提交的数据，对数据进行处理
        form =homepage.forms.LiuyanForm(request.POST)
        if form.is_valid():
            new_liuyan= form.save(commit=False)

            new_liuyan.owner = request.user
            new_liuyan.save()
            return HttpResponseRedirect(reverse('liuyan'))
    context ={'form':form,'liuyans':liuyans}
    return render(request,'bbs.html',context)