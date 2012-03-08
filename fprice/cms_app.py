from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _
from fprice.menu import PriceMenu

class PriceApp(CMSApp):
    name = _("Price App") # give your app a name, this is required
    urls = ["fprice.urls"] # link your app to url configuration(s)
    menus = [PriceMenu]

apphook_pool.register(PriceApp) # register your app
