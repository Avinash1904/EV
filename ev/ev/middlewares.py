from django.urls import reverse
from django.http import Http404


class RestrictStaffToAdminMiddleware(object):
    """
    A middleware to restrict /admin access
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_request(self, request):
        if request.path.startswith(reverse("admin:index")):
            if request.user.is_authenticated():
                if not request.user.is_superuser:
                    raise Http404
            else:
                raise Http404
