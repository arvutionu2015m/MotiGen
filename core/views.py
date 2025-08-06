from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignupForm, LoginForm, CVForm
from .utils import generate_ai_response
from .models import CVEntry
from .forms import CVForm, CVUploadForm
from .utils import generate_ai_response, extract_text_from_file

from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from .models import CVEntry
from django.shortcuts import get_object_or_404
from django.contrib import messages

@login_required
def delete_entry(request, entry_id):
    entry = get_object_or_404(CVEntry, id=entry_id, user=request.user)
    entry.delete()
    messages.success(request, "Sisestus kustutatud.")
    return redirect('dashboard')

@login_required
def view_entry(request, entry_id):
    entry = get_object_or_404(CVEntry, id=entry_id, user=request.user)
    return render(request, 'entry_detail.html', {'entry': entry})


@login_required
def download_pdf(request, entry_id):
    try:
        entry = CVEntry.objects.get(id=entry_id, user=request.user)
    except CVEntry.DoesNotExist:
        return HttpResponse("Not found", status=404)

    html_string = render_to_string('pdf_template.html', {'entry': entry})
    html = HTML(string=html_string)
    pdf = html.write_pdf()

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="AI_vastus_{entry.created_at.date()}.pdf"'
    return response


def home(request):
    return render(request, 'home.html')

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(request,
                                username=form.cleaned_data['username'],
                                password=form.cleaned_data['password'])
            if user:
                login(request, user)
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

from .models import CVEntry

@login_required
def generate_content(request):
    response = ""
    text_form = CVForm()
    upload_form = CVUploadForm()

    if request.method == 'POST':
        if 'cv_text' in request.POST:
            text_form = CVForm(request.POST)
            if text_form.is_valid():
                cv_data = text_form.cleaned_data['cv_text']
                response = generate_ai_response(cv_data)

                CVEntry.objects.create(user=request.user, content=cv_data, ai_response=response)
                messages.success(request, "AI vastus genereeritud tekstisisestusest.")
                return redirect('dashboard')

        elif 'cv_file' in request.FILES:
            upload_form = CVUploadForm(request.POST, request.FILES)
            if upload_form.is_valid():
                file = upload_form.cleaned_data['cv_file']
                try:
                    cv_data = extract_text_from_file(file)
                except Exception as e:
                    messages.error(request, f"Viga faili töötlemisel: {e}")
                    return redirect('generate_content')

                response = generate_ai_response(cv_data)

                CVEntry.objects.create(user=request.user, content=cv_data, ai_response=response)
                messages.success(request, "AI vastus genereeritud faili põhjal.")
                return redirect('dashboard')

    return render(request, 'generate.html', {
        'form': text_form,
        'upload_form': upload_form,
        'response': response
    })


@login_required
def dashboard(request):
    entries = CVEntry.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'dashboard.html', {'entries': entries})

