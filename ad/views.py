from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse
import json

from .models import Ad
from django.contrib.auth.models import User

@csrf_exempt
@login_required
def create_ad(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            ad = Ad.objects.create(
                user=request.user,
                title=data['title'],
                description=data['description'],
                image_url=data.get('image_url', ''),
                category=data['category'],
                condition=data['condition']
            )
            return JsonResponse({
                'message': 'Ad created successfully',
                'ad': {
                    'id': ad.id,
                    'title': ad.title,
                    'description': ad.description,
                    'image_url': ad.image_url,
                    'category': ad.category,
                    'condition': ad.condition,
                    'created_at': ad.created_at,
                }
            }, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Only POST allowed'}, status=405)
