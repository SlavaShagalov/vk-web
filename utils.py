from django.core.paginator import Paginator


def paginate(objects, request, per_page=5):
    per_page = 5 if per_page <= 0 else per_page

    paginator = Paginator(objects, per_page)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return page
