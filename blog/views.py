from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from blog.models import Article


class ArticleListView(ListView):
    model = Article
    template_name = "blog/article_list.html"
    context_object_name = "articles"

    def get_queryset(self):
        # Контент-менеджеры видят все статьи
        if self.request.user.has_perm('blog.can_publish_article'):
            return Article.objects.all().order_by('-created_at')
        # Обычные пользователи видят только опубликованные
        return Article.objects.filter(is_published=True).order_by('-created_at')


class ArticleDetailView(DetailView):
    model = Article
    template_name = "blog/article_detail.html"
    context_object_name = "article"

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)

        # Проверка: если статья не опубликована, только контент-менеджер может её смотреть
        if not self.object.is_published and not self.request.user.has_perm('blog.can_publish_article'):
            messages.error(self.request, 'Статья не опубликована или недоступна')
            return redirect('blog:article_list')

        self.object.views_count += 1
        self.object.save()
        return self.object


class ArticleCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Article
    fields = ["title", "text", "preview"]  # убрал is_published
    template_name = "blog/article_update.html"
    success_url = reverse_lazy("blog:article_list")
    permission_required = ['blog.add_article']

    def handle_no_permission(self):
        messages.error(self.request, 'У вас нет прав на создание статей')
        return redirect('blog:article_list')

    def form_valid(self, form):
        form.instance.is_published = False
        form.instance.owner = self.request.user
        messages.success(self.request, 'Статья создана и отправлена на модерацию')
        return super().form_valid(form)


class ArticleUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Article
    fields = ["title", "text", "preview"]
    template_name = "blog/article_update.html"
    success_url = reverse_lazy("blog:article_list")
    permission_required = ['blog.change_article']

    def handle_no_permission(self):
        messages.error(self.request, 'У вас нет прав на редактирование статей')
        return redirect('blog:article_list')


class ArticleDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Article
    template_name = "blog/article_confirm_delete.html"
    success_url = reverse_lazy("blog:article_list")
    permission_required = ['blog.delete_article']

    def handle_no_permission(self):
        messages.error(self.request, 'У вас нет прав на удаление статей')
        return redirect('blog:article_list')


class ArticlePublishView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = ['blog.can_publish_article']

    def post(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        article.is_published = True
        article.save()
        messages.success(request, f'Статья "{article.title}" опубликована')
        return redirect('blog:article_detail', pk=pk)

    def handle_no_permission(self):
        messages.error(self.request, 'У вас нет прав на публикацию статей')
        return redirect('blog:article_list')


class ArticleUnpublishView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = ['blog.can_unpublish_article']

    def post(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        article.is_published = False
        article.save()
        messages.success(request, f'Статья "{article.title}" снята с публикации')
        return redirect('blog:article_detail', pk=pk)

    def handle_no_permission(self):
        messages.error(self.request, 'У вас нет прав на снятие статей с публикации')
        return redirect('blog:article_list')