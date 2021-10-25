from django.core.paginator import Paginator

from yatube.settings import PAGINATOR_PAGE


def create_paginator(request, object):
    paginator = Paginator(object, PAGINATOR_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj
