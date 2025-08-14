from django.shortcuts import render

# Create your views here.
import random, string
from django.shortcuts import render, redirect, get_object_or_404
from .forms import URLForm
from .models import URL

def generate_short_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def home(request):
    form = URLForm()
    short_url = None
    if request.method == 'POST':
        form = URLForm(request.POST)
        if form.is_valid():
            original_url = form.cleaned_data['original_url']
            # Check if already exists
            try:
                url = URL.objects.get(original_url=original_url)
            except URL.DoesNotExist:
                short_code = generate_short_code()
                while URL.objects.filter(short_code=short_code).exists():
                    short_code = generate_short_code()
                url = URL(original_url=original_url, short_code=short_code)
                url.save()
            short_url = request.build_absolute_uri(f'/{url.short_code}')
            return render(request, 'shortener/result.html', {'short_url': short_url})
    return render(request, 'shortener/home.html', {'form': form})

def redirect_url(request, short_code):
    url = get_object_or_404(URL, short_code=short_code)
    return redirect(url.original_url)