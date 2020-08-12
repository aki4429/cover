from django.shortcuts import render

def loc_list(request):
    return render(request, 'loc/loc_list.html', {})
