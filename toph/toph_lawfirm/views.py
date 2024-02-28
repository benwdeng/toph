from django.shortcuts import render, redirect, get_object_or_404
from .models import Entry
from .forms import EntryForm
from django.http import JsonResponse

def entry_list(request):
    if request.method == 'POST':
        form = EntryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('entry_list')
    else:
        form = EntryForm()
    entries = Entry.objects.all()
    return render(request, 'toph_lawfirm/entry_list.html', {'form': form, 'entries': entries})

def edit_entry(request, pk):
    entry = get_object_or_404(Entry, pk=pk)
    if request.method == "POST":
        form = EntryForm(request.POST, request.FILES, instance=entry)
        if form.is_valid():
            form.save()
            return redirect('entry_detail', pk=entry.pk)  # Redirect to the entry's detail view or another appropriate view
    else:
        form = EntryForm(instance=entry)
    return render(request, 'toph_lawfirm/edit_entry.html', {'form': form})

def entry_detail(request, pk):
    entry = get_object_or_404(Entry, pk=pk)
    return render(request, 'toph_lawfirm/entry_detail.html', {'entry': entry})

def delete_entry(request, pk):
    entry = Entry.objects.get(pk=pk)
    entry.delete()
    return redirect('entry_list')  # Redirect to your entries list view

def entry_details(request, pk):
    entry = Entry.objects.get(pk=pk)
    return JsonResponse({
        'name': entry.name,
        'document_url': entry.document.url,
        # Add more fields as necessary
    })
