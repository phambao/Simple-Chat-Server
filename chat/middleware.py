from uuid import uuid4


class UserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        # Assign uuid for each user
        user_uuid = request.session.get('user_uuid', str(uuid4()))
        request.session['user_uuid'] = user_uuid

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
