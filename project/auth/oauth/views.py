from django.http import JsonResponse
from oauth2_provider.decorators import protected_resource


@protected_resource()
def userinfo(request):
    user = request.resource_owner
    if user.is_authenticated:
        user_data = {
            'public_id': user.public_id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'role': user.role,
        }
        return JsonResponse(user_data)

    return JsonResponse({'error': 'Unauthorized'}, status=401)