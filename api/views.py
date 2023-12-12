from django.contrib.auth import login, logout
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.conf import settings

from .forms import LoginForm, RegisterForm, ModifyForm
from .models import Article, ArticleCategory


def main_spa(request: HttpRequest) -> HttpResponse:
    return render(request, 'api/spa/index.html', {})


@require_http_methods(['POST', 'GET'])
def login_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            login(request, form.user_cache)
            return redirect(to='home')
    else:
        form = LoginForm()

    return render(request, 'api/auth/login.html', {'form': form})


@require_http_methods(['POST', 'GET'])
def register_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(to='home')
    else:
        form = RegisterForm()

    return render(request, 'api/auth/register.html', {'form': form})


@require_http_methods(['POST'])
def logout_view(request: HttpRequest) -> HttpResponse:
    logout(request)
    return HttpResponse(status=200)


@require_http_methods(['GET', 'POST'])
def profile_view(request: HttpRequest) -> HttpResponse:
    if not request.user.is_authenticated:
        return HttpResponse(status=401)

    if request.method == 'GET':
        return JsonResponse(status=200, data=serialize_user(request))
    else:
        form = ModifyForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return JsonResponse(status=200, data=serialize_user(request))
        else:
            return JsonResponse(status=400, data=form.errors.as_json(), safe=False)


@require_http_methods(['PUT'])
def category_view(request: HttpRequest, category_id: int) -> HttpResponse:
    if not request.user.is_authenticated:
        return HttpResponse(status=401)
    category = get_object_or_404(ArticleCategory, id=category_id)

    favourite_categories = request.user.favourite_categories
    if category in favourite_categories.all():
        favourite_categories.remove(category)
    else:
        favourite_categories.add(category)

    return JsonResponse(status=200, data=serialize_user(request))


@require_http_methods(['GET'])
def article_view(request: HttpRequest) -> HttpResponse:
    articles = Article.objects.order_by('created_at')
    articles = [article.to_dict() for article in articles]

    categories = ArticleCategory.objects.all()
    categories = [category.to_dict() for category in categories]

    response = {
        'categories': categories,
        'articles': articles
    }

    return JsonResponse(status=200, data=response, safe=False)


def serialize_user(request: HttpRequest):
    profile_url = request.build_absolute_uri(
        settings.MEDIA_URL + str(request.user.profile_image)
    ) if request.user.profile_image else None

    return {
        'id': request.user.id,
        'username': request.user.username,
        'email': request.user.email,
        'profile_url': profile_url,
        'date_of_birth': request.user.date_of_birth,
        'favourite_categories': list(request.user.favourite_categories.values('id', 'name'))
    }
