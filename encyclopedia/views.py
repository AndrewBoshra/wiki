import random
from django.urls import reverse
from django.http.response import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core.files.storage import default_storage
import os.path
from django.urls.conf import include  
import markdown2 
from . import util
import django.forms

class pagef(django.forms.forms.Form):
    title=django.forms.CharField(widget=django.forms.TextInput(
        attrs={
            "class":"form-control"
        }
        ))
    content=django.forms.CharField(widget=django.forms.Textarea(
        attrs={
            "class":"form-control"
        }
    ))
class editpagef(django.forms.forms.Form):
    content=django.forms.CharField(widget=django.forms.Textarea(
        attrs={
            "class":"form-control"
        }
    ))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def viewpage(request,title):
    if title in util.list_entries():
        PATH=os.path.join(default_storage.path("entries"),title+".md")
        return render(request,"encyclopedia/page.html",{
            "pagetitle" : title,
            "content" : markdown2.markdown_path(PATH)  
        })
    return HttpResponseRedirect(reverse("notfound"))

def notfound(request):
    return render(request,"encyclopedia/404.html",status=404)

def search(request):
    if request.method=="GET":
        search_query=request.GET["q"] 
        result=util.search_for_entry(search_query)
        if len(result)== 1:
            return HttpResponseRedirect(reverse('viewpage',args=[result[0]])) 
        return render(request,"encyclopedia/search_result.html",
        {
            "query":search_query
            ,"results":result
        })       


def newpage(request):
    if request.method=='POST':
        created_page=pagef(request.POST)
        if created_page.is_valid() and not util.exist(created_page.cleaned_data["title"]):
            util.save_entry(created_page.cleaned_data["title"],created_page.cleaned_data["content"])
            return HttpResponseRedirect(reverse(viewpage,args=[created_page.cleaned_data["title"]]))
        else:
            response=render(request,"encyclopedia/newpage.html",{"page":created_page})
            return response


    return render(request,"encyclopedia/newpage.html",{"page":pagef()})

def editpage(request,title):

    if not util.exist(title):
        return HttpResponseRedirect(reverse(notfound))
    
    if request.method=='GET':
        pagecont =editpagef(initial={'title':title ,'content':util.get_entry(title)  })
        return render(request,"encyclopedia/edit_page.html",{"title":title ,"page":pagecont})
        
    else:
        edited_page=editpagef(request.POST)
        if edited_page.is_valid():
            util.save_entry(title,edited_page.cleaned_data["content"])
            return HttpResponseRedirect(reverse(viewpage,args=[title]))

def rand_page(request):
    return HttpResponseRedirect(reverse(viewpage,args=[random.choice(util.list_entries())]))