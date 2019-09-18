from django.urls import path

from {{cookiecutter.project_slug}}.users.views import (
    user_redirect_view,
    user_update_view,
    user_detail_view,
    current_user_detail_view
)

app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("/", view=current_user_detail_view, name="detail"),
    path("<str:email>/", view=user_detail_view, name="detail"),
]
