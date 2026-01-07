from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("outfits/new/", views.create_outfit_plan, name="create_outfit_plan"),
    path("outfits/plan-week/", views.plan_this_week, name="plan_this_week"),
    path("week/", views.week_view, name="week_view"),
    path("outfits/<int:plan_id>/", views.outfit_detail, name="outfit_detail"),
    path("outfits/<int:plan_id>/edit/", views.edit_outfit_plan, name="edit_outfit_plan"),
    path("outfits/<int:plan_id>/add-item/", views.add_look_item, name="add_look_item"),
    path("feed/", views.public_feed, name="public_feed"),
    path("feed/<int:plan_id>/", views.public_outfit_detail, name="public_outfit_detail"),
    path("admin/outfits/<int:plan_id>/delete/", views.admin_delete_any_outfit, name="admin_delete_any_outfit"),
    path("outfits/<int:plan_id>/delete/", views.delete_outfit_plan, name="delete_outfit_plan"),
    
]
