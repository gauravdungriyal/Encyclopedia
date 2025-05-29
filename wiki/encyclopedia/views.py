import markdown2
import html2text
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import Http404
from django import forms
from django.urls import reverse

from . import util

class NewTaskForm(forms.Form):
    title=forms.CharField(label="Name")
    description=forms.CharField(widget=forms.Textarea, label="Description")

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wiki(request,title):
    entries=util.list_entries()
    if title.capitalize() in entries:
        title=title.capitalize()
        with open(f"entries/{title}.md","r") as md_file:
            markdownContent=md_file.read()
            html=markdown2.markdown(markdownContent)
            return render(request,"encyclopedia/mainfile.html",{
                "name":title,
                "data":html
            })
    elif title.lower() in entries:
        title=title.lower()
        with open(f"entries/{title}.md","r") as md_file:
            markdownContent=md_file.read()
            html=markdown2.markdown(markdownContent)
            return render(request,"encyclopedia/mainfile.html",{
                "name":title,
                "data":html
            })
    elif title.upper() in entries:
        title=title.upper()
        with open(f"entries/{title}.md","r") as md_file:
            markdownContent=md_file.read()
            html=markdown2.markdown(markdownContent)
            return render(request,"encyclopedia/mainfile.html",{
                "name":title,
                "data":html
            })
    else:
        raise Http404("requested page was not found.")

def search(request):
    entries=util.list_entries()
    title=request.GET.get('q')
    if title.capitalize() in entries:
        title=title.capitalize()
        with open(f"entries/{title}.md","r") as md_file:
            markdownContent=md_file.read()
            html=markdown2.markdown(markdownContent)
            return HttpResponse(html)
    elif title.lower() in entries:
        title=title.lower()
        with open(f"entries/{title}.md","r") as md_file:
            markdownContent=md_file.read()
            html=markdown2.markdown(markdownContent)
            return HttpResponse(html)
    elif title.upper() in entries:
        title=title.upper()
        with open(f"entries/{title}.md","r") as md_file:
            markdownContent=md_file.read()
            html=markdown2.markdown(markdownContent)
            return HttpResponse(html)
    else:
        ls=[]
        for entry in entries:
            if title.capitalize() in entry or title.lower() in entry or title.upper() in entry:
                ls.append(entry)
        if not ls:
            return HttpResponse("Not Exist")
        else:
            return render(request,"encyclopedia/search.html",{
                "ls":ls
            })

def createpage(request):
    if request.method=="POST":
        form=NewTaskForm(request.POST)
        if form.is_valid():
            text=form.cleaned_data["description"]
            name=form.cleaned_data["title"]
            try:
             with open(f"entries/{name}.md","x") as md:
                md.write(text)
                return HttpResponseRedirect(reverse("index"))
            except:
                return HttpResponse("File Aready Exist!")

            
        else:
             return render(request,"encyclopedia/createPage.html",{
                 "form":NewTaskForm()  
                })
            
    return render(request,"encyclopedia/createPage.html",{
      "form":NewTaskForm()  
    })

def editpage(request,title):
    if request.method=="POST":
        edited_data=request.POST.get('edited_text')
        with open(f"entries/{title}.md","w") as md:
            md.write(edited_data)
            return HttpResponseRedirect(reverse("index"))
    with open(f"entries/{title}.md") as md:
        text=md.read()
        return render(request,"encyclopedia/editPage.html",{
            "form":NewTaskForm(),
            "text":text,
            "title":title
        })





