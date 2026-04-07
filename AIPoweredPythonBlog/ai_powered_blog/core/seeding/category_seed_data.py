CATEGORY_DEFINITIONS = [
    {"name": ".NET Ecosystem", "slug": "dotnet-ecosystem", "sort_order": 1},
    {"name": "Python Ecosystem", "slug": "python-ecosystem", "sort_order": 2},
    {"name": "Cloud (Azure & AWS)", "slug": "cloud-azure-aws", "sort_order": 3},
    {"name": "DevOps & Automation", "slug": "devops-automation", "sort_order": 4},
    {"name": "Containers and Kubernetes", "slug": "containers-and-kubernetes", "sort_order": 5},
    {"name": "Infrastructure as Code", "slug": "infrastructure-as-code", "sort_order": 6},
    {"name": "Architecture and Patterns", "slug": "architecture-and-patterns", "sort_order": 7},
]


def seed_categories(CategoryModel, stdout, style):
    categories = {}

    for item in CATEGORY_DEFINITIONS:
        category, created = CategoryModel.objects.get_or_create(
            slug=item["slug"],
            defaults={
                "name": item["name"],
                "sort_order": item["sort_order"],
            },
        )

        changed = False

        if category.name != item["name"]:
            category.name = item["name"]
            changed = True

        if category.sort_order != item["sort_order"]:
            category.sort_order = item["sort_order"]
            changed = True

        if changed:
            category.save(update_fields=["name", "sort_order"])

        if created:
            stdout.write(style.SUCCESS(f"Created category: {category.name}"))
        elif changed:
            stdout.write(f"Updated category: {category.name}")
        else:
            stdout.write(f"Category already exists: {category.name}")

        categories[item["slug"]] = category

    return categories
