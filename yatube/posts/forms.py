from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group')

    def clean_subject(self):
        data = self.cleaned_data['text']
        print(data)
        if data == '':
            raise forms.ValidationError('Пост должен содержать какой-то текст')

        return data
