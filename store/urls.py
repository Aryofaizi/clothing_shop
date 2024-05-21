from django.urls import path
from . import views
urlpatterns = [
    path("", views.HomeView.as_view(), name="home_page"),
    path("products/<int:pk>/", views.ProductDetailView.as_view(), name="product_detail"),
    path("comment/<int:pk>/", views.CommentCreateView.as_view(), name="comment_create"),
    path("category/<int:pk>/", views.CategroyList.as_view(), name="category_list"),
    path("category/search/", views.CategorySearchList.as_view(), name="category_search"),
    path("user_dashboard/", views.UserDashboard.as_view(), name="user_dashboard"),
    path("about/", views.about, name="about_page"),
    path("contact/", views.contact, name="contact_page"),
]
