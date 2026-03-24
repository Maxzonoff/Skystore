from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

from blog.models import Article


class ArticleListView(ListView):
    model = Article
    template_name = 'blog/article_list.html'
    context_object_name = 'articles'

    def get_queryset(self):
        return Article.objects.filter(is_published=True)


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'blog/article_detail.html'
    context_object_name = 'article'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object


class ArticleCreateView(CreateView):
    model = Article
    fields = ["title", "text", "preview", "is_published"]
    template_name = 'blog/article_form.html'
    success_url = reverse_lazy("blog:article_list")


class ArticleUpdateView(UpdateView):
    model = Article
    fields = ["title", "text", "preview", "is_published"]
    template_name = 'blog/article_form.html'
    success_url = reverse_lazy("blog:article_list")

    def get_success_url(self):
        return reverse('blog:article_detail', args=[self.object.pk])


class ArticleDeleteView(DeleteView):
    model = Article
    template_name = 'blog/article_confirm_delete.html'
    success_url = reverse_lazy("blog:article_list")
