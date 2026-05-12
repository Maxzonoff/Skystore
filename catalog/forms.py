from django import forms
from django.core.exceptions import ValidationError
from django.forms import BooleanField

from catalog.models import Product


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs["class"] = "form-check-input"
            else:
                field.widget.attrs["class"] = "form-control"


class ProductForm(forms.ModelForm):
    list_words = [
        "казино",
        "криптовалюта",
        "крипта",
        "биржа",
        "дешево",
        "бесплатно",
        "обман",
        "полиция",
        "радар",
    ]

    class Meta:
        model = Product
        fields = "__all__"
        widgets = {
            "image": forms.ClearableFileInput(
                attrs={
                    "class": "form-control-file custom-file-input",
                    "style": "background-color: #007bff; color: white; padding: 8px 16px; border-radius: 4px;",
                }
            )
        }

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите наименование товара"}
        )
        self.fields["description"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите описание товара"}
        )
        self.fields["image"].widget.attrs.update({"class": "form-control"})
        self.fields["category"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Выберите категорию"}
        )
        self.fields["price"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Укажите стоимость товара"}
        )

    def clean_price(self):
        price = self.cleaned_data["price"]
        if price < 0:
            raise ValidationError("Цена не может быть отрицательной")
        return price

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if not name:
            return name
        for word in self.list_words:
            if word.lower() in name.lower():
                raise ValidationError(
                    f"Название товара не может содержать слово {word}!"
                )
        return name

    def clean_description(self):
        description = self.cleaned_data.get("description")
        if not description:
            return description
        for word in self.list_words:
            if word.lower() in description.lower():
                raise ValidationError(
                    f"Описание товара не может содержать слово {word}!"
                )
        return description
