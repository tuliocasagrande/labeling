from django.template import Library
register = Library()


@register.assignment_tag(takes_context=True)
def user_is_owner(context):
    request = context['request']
    dataset = context['dataset']
    return dataset.is_owned_by(request.user)
