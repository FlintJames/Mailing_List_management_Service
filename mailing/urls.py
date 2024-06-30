from django.urls import path
from django.views.decorators.cache import cache_page

from mailing.apps import MailingConfig
from mailing.views import BlogDetailView, BlogCreateView, BlogUpdateView, BlogDeleteView, \
    toggle_publication, BlogListView, ClientListView, ClientCreateView, ClientDeleteView, ClientUpdateView, \
    ClientDetailView

app_name = MailingConfig.name

urlpatterns = [
    path('', ClientListView.as_view(), name='client_list'),
    path('client/<int:pk>/', cache_page(60)(ClientDetailView.as_view()), name='client_detail'),
    path('client/create/', ClientCreateView.as_view(), name='client_create'),
    path('client/<int:pk>/update', ClientUpdateView.as_view(), name='client_update'),
    path('client/<int:pk>/delete', ClientDeleteView.as_view(), name='client_delete'),
    path("mailing/", BlogListView.as_view(), name='blog_list'),
    path("blog/<int:pk>/", BlogDetailView.as_view(), name='blog_detail'),
    path("blog/create/", BlogCreateView.as_view(), name='blog_create'),
    path("blog/<int:pk>/update/", BlogUpdateView.as_view(), name='blog_update'),
    path("blog/<int:pk>/delete/", BlogDeleteView.as_view(), name='blog_delete'),
    path("publication/<int:pk>/", toggle_publication, name='toggle_publication')
]
