def username_processor(request):
    return {'username': request.user.username if request.user.is_authenticated else None}
