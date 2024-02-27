from django.shortcuts import render, redirect
from django.http import FileResponse
from .models import Document
from .forms import DocumentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate

@login_required
def document_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('document_upload')
    else:
        form = DocumentForm()
    return render(request, 'myapp/document_upload.html', {'form': form})

def document_download(request, pk):
    document = Document.objects.get(pk=pk)
    response = FileResponse(document.uploaded_file)
    return response


def landing_page(request):
    return render(request, 'landing_page.html')
