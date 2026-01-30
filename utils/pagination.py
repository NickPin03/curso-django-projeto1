import math
from django.core.paginator import Paginator


def make_pagination_range(
    page_range,
    qty_pages,
    current_page,
):
    middle_range = math.ceil(qty_pages / 2)
    start_range = current_page - middle_range
    stop_range = current_page + middle_range
    total_pages = len(page_range)

    start_range_offset = abs(start_range) if start_range < 0 else 0

    if start_range < 0:
        start_range = 0
        stop_range += start_range_offset

    if stop_range >= total_pages:
        start_range = start_range - abs(total_pages - stop_range)

    pagination = page_range[start_range:stop_range]
    return {
        "pagination": pagination,
        "page_range": page_range,
        "qty_pages": qty_pages,
        "current_page": current_page,
        "total_pages": total_pages,
        "start_range": start_range,
        "stop_range": stop_range,
        "first_page_out_of_range": current_page > middle_range,
        "last_page_out_of_range": stop_range < total_pages,
    }


def make_pagination(request, queryset, per_page, qty_pages=4):
    try:
        current_page = int(
            request.GET.get("page", 1)
        )  ## pega só a página que user digitou na  URL
    except ValueError:
        current_page = 1

    paginator = Paginator(
        queryset, per_page
    )  ## pega todas as recipes  armazenadas no objeto recipes e divide elas em 9 receitas por página
    page_obj = paginator.get_page(
        current_page
    )  ## Dividiu em 11 páginas, obj retorna pag atual

    pagination_range = make_pagination_range(  ## para mostrar apenas 4 números de páginas para escolher por vez dependendo de onde está -  lista de números que devem aparecer
        paginator.page_range, qty_pages, current_page
    )  ## Garante que o usuário não fique confuso vendo 100 botões de página. Ele mostra apenas um "pedacinho" do menu.

    return page_obj, pagination_range
