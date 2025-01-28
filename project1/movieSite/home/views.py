from django.shortcuts import render

#returns the rendered HOME template when called
#AS OF WRITING, TEMPLATE IS NOT FINAL (please update when template is made)
def index(request):
    return render(request, 'home/index.html')