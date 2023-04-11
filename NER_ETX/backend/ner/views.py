from django.shortcuts import render

# Create your views here.

from django.http import JsonResponse
from .models import Paragraph

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def process_paragraphs(request):
    if request.method == 'POST':
        paragraphs = request.POST.dict()
        modified_paragraphs = []

        for key,value in paragraphs.items():
            modified_paragraphs.append(value.upper())
        
        return JsonResponse({'modified_paragraphs': modified_paragraphs})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
