from django.shortcuts import render

# Create your views here.
from user.views import check_cookie_user_id


@check_cookie_user_id
def index(request):
    return render(request, "index.html")

