from django import template
# В template.Library зарегистрированы все встроенные теги и фильтры шаблонов;
# добавляем к ним и наш фильтр.
register = template.Library()


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={'class': css})


@register.filter()
def addmessage(field, text):
    '''Change error message in the form.'''

    oninvalid = f"this.setCustomValidity('{text}')"
    oninput = "setCustomValidity('')"
    return field.as_widget(attrs={'oninvalid': oninvalid, 'oninput': oninput})


@register.filter
def addclassandmessage(field, css_and_text):
    '''Filter for adding class to field and change error message to form.

    Please, classes and message indicate through sign ":"
    and write the error message in the end of css_text variable

    '''

    css_and_text = css_and_text.split(':')
    css = ' '.join(css_and_text[:-1])
    text = css_and_text[-1]
    oninvalid = f"this.setCustomValidity('{text}')"
    oninput = "setCustomValidity('')"
    return field.as_widget(attrs={'class': css,
                                  'oninvalid': oninvalid,
                                  'oninput': oninput})
