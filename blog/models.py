from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок статьи', help_text='Укажите заголовок')
    text = models.TextField(verbose_name='Содержание', help_text='Напишите содержание')
    preview = models.ImageField(
        upload_to="articles/",
        verbose_name="Превью",
        help_text="Загрузите превью статьи",
        null=True,
        blank=True, )
    created_at = models.DateField(auto_now_add=True)
    is_published = models.BooleanField(default=True)
    views_count = models.PositiveIntegerField(default=0)


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'статья'
        verbose_name_plural = 'статьи'