from wagtail import hooks


@hooks.register("construct_main_menu")
def hide_unneeded_menu_items(request, menu_items):
    hidden_names = {"help"}
    menu_items[:] = [item for item in menu_items if item.name not in hidden_names]
