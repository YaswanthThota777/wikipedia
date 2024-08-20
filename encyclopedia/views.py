from django.shortcuts import render,redirect
from django.contrib import messages
from . import util
import markdown
import random

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    entry_content = util.get_entry(title)

    if entry_content is None:
        return render(request, "encyclopedia/error.html", {
            "message": "Entry not found."
        })
    else:
        content_html = markdown.markdown(entry_content)
        
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": content_html
        })


def search(request):
    query = request.GET.get('q', '').strip()
    entries = util.list_entries()
    
    if query:
        if query in entries:
            return redirect('entry', title=query)
        
        matching_entries = [entry for entry in entries if query.lower() in entry.lower()]
    else:
        matching_entries = []

    return render(request, "encyclopedia/search_results.html", {
        "query": query,
        "entries": matching_entries
    })



def create_entry(request):
    if request.method == "POST":
        title = request.POST.get('title').strip()
        content = request.POST.get('content')
        
        if not title:
            messages.error(request, "Title is required.")
            return render(request, "encyclopedia/create_entry.html")
        
        if util.get_entry(title) is not None:
            messages.error(request, "An entry with this title already exists.")
            return render(request, "encyclopedia/create_entry.html")
        
        util.save_entry(title, content)
        return redirect('entry', title=title)
    
    return render(request, "encyclopedia/create_entry.html")


def edit_entry(request, title):
    if request.method == "POST":
        new_content = request.POST.get('content')
        
        if new_content is None:
            messages.error(request, "Content cannot be empty.")
            return render(request, "encyclopedia/edit_entry.html", {
                "title": title,
                "content": util.get_entry(title)
            })
        
        util.save_entry(title, new_content)
        return redirect('entry', title=title)
    
    content = util.get_entry(title)
    if content is None:
        messages.error(request, "Entry not found.")
        return redirect('index')
    
    return render(request, "encyclopedia/edit_entry.html", {
        "title": title,
        "content": content
    })


def random_page(request):
    entries = util.list_entries()
    if not entries:
        return redirect('index')  
    random_entry = random.choice(entries)
    return redirect('entry', title=random_entry)