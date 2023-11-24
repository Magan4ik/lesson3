from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import redirect, reverse


@login_required
@require_http_methods(["GET"])
def search_view(request: HttpRequest) -> HttpResponse:
    option = request.GET.get("option")
    search = request.GET.get("search", '')

    if option == "weather":
        url = reverse('weather:weather_search')
        return redirect(f"{url}?search={search}")
    else:
        url = reverse('blog:post_list')
        return redirect(f"{url}?search={search}")