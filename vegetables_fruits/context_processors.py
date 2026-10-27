from .models import ProgressionJunior


def progression_junior(request):
    if request.user.is_authenticated and hasattr(request.user, 'mode_junior') and request.user.mode_junior:
        progression, _ = ProgressionJunior.objects.get_or_create(user=request.user)
        return {'progression': progression}
    return {'progression': None}