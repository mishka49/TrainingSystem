from django.urls import path

from products.views import UserView, ProductView, LessonView, UserProducts, GroupsCompoundView, ProductUsersGroupsView

urlpatterns = [
    path('user/', UserView.as_view()),
    path('products/', ProductView.as_view()),
    path('product_users_groups/<str:product>', ProductUsersGroupsView.as_view()),
    path('lesson/', LessonView.as_view()),
    path('users_products/<str:user>', UserProducts.as_view()),
    path('groups_compound/<str:product>', GroupsCompoundView.as_view()),
]
