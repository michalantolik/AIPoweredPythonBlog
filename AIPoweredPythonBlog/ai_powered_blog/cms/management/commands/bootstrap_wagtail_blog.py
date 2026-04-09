from django.core.management.base import BaseCommand
from wagtail.models import Page, Site

from cms.models import BlogIndexPage


class Command(BaseCommand):
    help = "Create the Wagtail blog index page if it does not exist."

    def handle(self, *args, **options):
        site = Site.objects.filter(is_default_site=True).first() or Site.objects.first()
        if site is None:
            self.stderr.write(self.style.ERROR("No Wagtail Site record exists."))
            return

        parent = site.root_page
        existing = BlogIndexPage.objects.child_of(parent).filter(slug="articles").first()

        if existing:
            self.stdout.write(self.style.SUCCESS("Blog index already exists at /articles/."))
            return

        page = BlogIndexPage(
            title="Articles",
            slug="articles",
            intro="Structured technical writing about software architecture, engineering, and delivery.",
        )
        parent.add_child(instance=page)
        page.save_revision().publish()

        self.stdout.write(self.style.SUCCESS("Created /articles/ blog index page."))
