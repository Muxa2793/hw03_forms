from django.conf.urls import url
from django.contrib import admin
from django.core.management import call_command
from django.http import HttpResponseRedirect

from .models import Group, Post


class PostAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'pub_date', 'author', 'group')
    list_editable = ('group',)
    search_fields = ('text', )
    list_filter = ('pub_date', 'group',)
    empty_value_display = '-пусто-'


class GroupAdmin(admin.ModelAdmin):
    change_list_template = 'admin/model_change_list.html'
    list_display = ('pk', 'title', 'slug', 'description')

    def get_urls(self):
        urls = super(GroupAdmin, self).get_urls()
        custom_urls = [
            url('^import/$', self.process_import, name='process_import'),
        ]
        return custom_urls + urls

    def process_import(self, request):
        try:
            file = request.FILES['filename']
            call_command("xlsx_group_import", file)
        except KeyError:
            pass
        return HttpResponseRedirect("../")


admin.site.register(Post, PostAdmin)
admin.site.register(Group, GroupAdmin)
