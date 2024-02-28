from django.shortcuts import render, redirect, get_object_or_404
from .models import Entry
from .forms import EntryForm
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.contrib.auth.decorators import login_required
from functools import wraps
from django.contrib.messages import get_messages


def group_required(group_name):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                # This check ensures we redirect unauthenticated users to login.
                messages.error(request, "Please login to access this page.")
                return redirect('toph_lawfirm_login')
            elif not request.user.groups.filter(name=group_name).exists():
                # Group check fails
                messages.error(request, "Access Denied. You do not have permission to access this page.")
                return redirect('toph_lawfirm_login')
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

@group_required('lawfirm_users')
def entry_list(request):
    print("entry_list view accessed by", request.user)
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
    else:
        form = EntryForm(instance=entry)
        return render(request, 'toph_lawfirm/edit_entry.html', {'form': form, 'entry': entry})

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
            'form_id': entry.form_id,
            'council': entry.council,
            'subject_land_address': entry.subject_land_address,
            'contact': entry.contact,
            'contact_role': entry.contact_role,
            'contact_postal_address': entry.contact_postal_address,
            'contact_number': entry.contact_number,
            'contact_email': entry.contact_email,
            'created_date': entry.created_date,
            'last_updated': entry.last_updated,
            'document_url': entry.document.url if entry.document else None,
        })
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Entry not found'}, status=404)
    


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm


def custom_login(request):
    # Clear previous messages
    storage = get_messages(request)
    for message in storage:
        # Optionally do something with the message
        pass
    storage.used = True  # Clear messages

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('entry_list')  # Adjust the redirect as needed
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'toph_lawfirm/login.html', {'form': form})


from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy

class custom_logout(LogoutView):
    next_page = reverse_lazy('landing_page')  



