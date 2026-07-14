from django.http import HttpResponse


class HealthCheckMiddleware:
    """
    Responde a /health/ inmediatamente sin pasar por el resto del middleware stack.
    Evita que Railway mate el proceso por healthcheck timeout mientras Django inicializa.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == '/health/':
            return HttpResponse("ok", status=200)
        return self.get_response(request)
