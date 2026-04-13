from django import template

register = template.Library()


@register.simple_tag
def pagination_items(page_obj, window=1, edges=1):
    """
    Build a compact pagination sequence.

    Example output:
    [1, '…', 4, 5, 6, '…', 10]
    """
    if not page_obj:
        return []

    current = page_obj.number
    total = page_obj.paginator.num_pages

    if total <= 1:
        return []

    pages = set()

    for page in range(1, min(edges, total) + 1):
        pages.add(page)

    for page in range(max(current - window, 1), min(current + window, total) + 1):
        pages.add(page)

    for page in range(max(total - edges + 1, 1), total + 1):
        pages.add(page)

    sorted_pages = sorted(pages)

    items = []
    previous = None

    for page in sorted_pages:
        if previous is not None and page - previous > 1:
            items.append("…")
        items.append(page)
        previous = page

    return items
