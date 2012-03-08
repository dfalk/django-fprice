from cms.menu_bases import CMSAttachMenu
from menus.base import Menu, NavigationNode
from menus.menu_pool import menu_pool
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from fprice.models import ProductCategory

class PriceMenu(CMSAttachMenu):
    name = _("Price Menu") # give the menu a name, this is required.

    def get_nodes(self, request):
        """
        This method is used to build the menu tree.
        """
        nodes = []
        return nodes
menu_pool.register_menu(PriceMenu) # register the menu.
