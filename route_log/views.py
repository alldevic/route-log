from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .forms import DocumentForm


@login_required
def index(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    else:
        form = DocumentForm()
    return render(request, 'route_log/index.html', {
        'form': form
    })
