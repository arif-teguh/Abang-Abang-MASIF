from django.shortcuts import render


# Create your views here.

def landing(request):
    try:
        return render(request, 'landing_page.html')
    except:
        print("There is an error")
