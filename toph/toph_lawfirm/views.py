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
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)


def entry_detail(request, pk):
    entry = get_object_or_404(Entry, pk=pk)
    return render(request, 'toph_lawfirm/entry_detail.html', {'entry': entry})

def delete_entry(request, pk):
    entry = Entry.objects.get(pk=pk)
    entry.delete()
    return redirect('entry_list')  # Redirect to your entries list view

def entry_details(request, pk):
    try:
        entry = Entry.objects.get(pk=pk)
        return JsonResponse({
            'name': entry.name,
            # Adjust this to match how your Entry model's document field can be accessed
            'document_url': entry.document.url if hasattr(entry.document, 'url') else ''
        })
    except Entry.DoesNotExist:
        return JsonResponse({'error': 'Entry not found'}, status=404)
