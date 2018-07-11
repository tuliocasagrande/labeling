from django.template import Library
register = Library()


@register.assignment_tag(takes_context=True)
def user_can_write(context):
    request = context['request']
    dataset = context['dataset']
    return dataset.is_writable_by(request.user)
