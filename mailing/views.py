from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from mailing.forms import ClientForm
from mailing.models import Client, Blog


class ClientListView(ListView, LoginRequiredMixin):
    model = Client
    success_url = reverse_lazy('mailing:client_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        return Client.objects.filter(owner=self.request.user)


class ClientDetailView(DetailView, LoginRequiredMixin):
    model = Client
    success_url = reverse_lazy('service:client_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        client_item = self.get_object()
        context['title'] = client_item.first_name
        return context


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:client_list')

    def form_valid(self, form):
        client = form.save()
        user = self.request.user
        client.owner = user
        client.save()
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:client_list')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user == self.object.owner or self.request.user.is_superuser:
            return self.object
        raise PermissionDenied


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('mailing:client_list')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user == self.object.owner or self.request.user.is_superuser:
            return self.object
        raise PermissionDenied


# class MessageListView(LoginRequiredMixin, ListView):
#     model = Message
#     fields = ['subject', 'text', 'picture']
#     template_name = 'service/message_list.html'
#     extra_context = {'title': 'Напишите сообщение'}

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         return context
#
#     def get_queryset(self):
#         return Message.objects.filter(owner=self.request.user)
#
#
# class MessageDetailView(LoginRequiredMixin, DetailView):
#     model = Message
#     fields = ['subject', 'text', 'picture']
#     template_name = 'service/message_detail.html'
#     success_url = reverse_lazy('service:message_list')
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         message_item = self.get_object()
#         context['title'] = message_item.subject
#         return context
#
#
# class MessageCreateView(LoginRequiredMixin, CreateView):
#     model = Message
#     fields = ['subject', 'text', 'picture']
#     template_name = 'service/message_form.html'
#     success_url = reverse_lazy('service:message_list')
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = 'Создание сообщения'
#         return context
#
#     def form_valid(self, form):
#         message = form.save()
#         user = self.request.user
#         message.owner = user
#         message.save()
#         return super().form_valid(form)
#
#
# class MessageUpdateView(LoginRequiredMixin, UpdateView):
#     model = Message
#     fields = ['subject', 'text', 'picture']
#     template_name = 'service/message_form.html'
#     success_url = reverse_lazy('service:message_list')
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         message_item = self.get_object()
#         context['title'] = message_item.subject
#         return context
#
#     def get_form_class(self):
#         user = self.request.user
#         if user == self.object.owner:
#             return MessageForm
#         if user.groups.filter(name='Manager').exists():
#             return MessageModeratorForm
#         raise PermissionDenied
#
#
# class MessageDeleteView(LoginRequiredMixin, DeleteView):
#     model = Message
#     fields = ['subject', 'text', 'picture']
#     template_name = 'service/message_confirm_delete.html'
#     success_url = reverse_lazy('service:message_list')
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         message_item = self.get_object()
#         context['title'] = message_item.subject
#         return context


class BlogListView(ListView):
    model = Blog


class BlogDetailView(DetailView):
    model = Blog

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_counter += 1
        self.object.save()
        return self.object


class BlogCreateView(CreateView):
    model = Blog
    fields = ("title", "content", "image", "publication_sign", "number_of_views")
    success_url = reverse_lazy('mailing:blog_list')


class BlogUpdateView(UpdateView):
    model = Blog
    fields = ("title", "content", "image", "publication_sign", "number_of_views")
    success_url = reverse_lazy('mailing:blog_list')

    def get_success_url(self):
        return reverse('mailing:blog_detail', args=[self.kwargs.get('pk')])


class BlogDeleteView(DeleteView):
    model = Blog
    success_url = reverse_lazy('mailing:blog_list')


def toggle_publication(request, pk):
    blog_item = get_object_or_404(Blog, pk=pk)
    if blog_item.publication_sign:
        blog_item.publication_sign = False
    else:
        blog_item.publication_sign = True

    blog_item.save()

    return redirect(reverse('mailing:blog_list'))
