from .models import Visitor

class VisitorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Verifica se existe session_key
        if not request.session.session_key:
            request.session.save()

        # Registra o visitante
        Visitor.get_or_create_visitor(request.session.session_key)

        response = self.get_response(request)
        return response