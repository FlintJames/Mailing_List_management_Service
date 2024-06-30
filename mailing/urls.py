from django.urls import path
from django.views.decorators.cache import cache_page

from mailing.apps import MailingConfig
from mailing.views import BlogDetailView, BlogCreateView, BlogUpdateView, BlogDeleteView, \
    toggle_publication, BlogListView, ClientListView, ClientCreateView, ClientDeleteView, ClientUpdateView, \
    ClientDetailView, MessageListView, MessageDetailView, MessageCreateView, MessageUpdateView, MessageDeleteView, \
    MailingListView, MailingDetailView, MailingCreateView, MailingUpdateView, MailingDeleteView, AttemptListView, \
    HomePage

app_name = MailingConfig.name

urlpatterns = [
    path('', HomePage.as_view(), name='statistics'),
    path('client/', ClientListView.as_view(), name='client_list'),
    path('client/<int:pk>/', ClientDetailView.as_view(), name='client_detail'),
    path('client/create/', ClientCreateView.as_view(), name='client_create'),
    path('client/<int:pk>/update', ClientUpdateView.as_view(), name='client_update'),
    path('client/<int:pk>/delete', ClientDeleteView.as_view(), name='client_delete'),

    path('message_list/', MessageListView.as_view(), name='message_list'),
    path('message/<int:pk>/', MessageDetailView.as_view(), name='message_detail'),
    path('message/create/', MessageCreateView.as_view(), name='message_create'),
    path('message/<int:pk>/update', MessageUpdateView.as_view(), name='message_update'),
    path('message/<int:pk>/delete', MessageDeleteView.as_view(), name='message_delete'),

    path('mailing_list/', MailingListView.as_view(), name='mailing_list'),
    path('mailing/<int:pk>/', MailingDetailView.as_view(), name='mailing_detail'),
    path('mailing_create/', MailingCreateView.as_view(), name='mailing_create'),
    path('mailing/<int:pk>/update', MailingUpdateView.as_view(), name='mailing_update'),
    path('mailing/<int:pk>/delete', MailingDeleteView.as_view(), name='mailing_delete'),

    path('mailing/<int:pk>/attempt/', AttemptListView.as_view(), name='attempt_list'),

    path("mailing/", BlogListView.as_view(), name='blog_list'),
    path("blog/<int:pk>/", BlogDetailView.as_view(), name='blog_detail'),
    path("blog/create/", BlogCreateView.as_view(), name='blog_create'),
    path("blog/<int:pk>/update/", BlogUpdateView.as_view(), name='blog_update'),
    path("blog/<int:pk>/delete/", BlogDeleteView.as_view(), name='blog_delete'),
    path("publication/<int:pk>/", toggle_publication, name='toggle_publication')
]
