
from django.contrib import admin
from django.urls import path , include
from store.views import index, product_detail,add_to_cart, cart,delete_cart
from django.conf.urls.static import static
from shop import settings
from accounts.views import signup
from accounts.views import logout_user
from accounts.views import login_user
from accounts.views import activate

from django.conf import settings

urlpatterns = [
   
    path('', index, name='index'),
    path('admin/', admin.site.urls),
    path('signup/', signup, name='signup'),
    path('logout/', logout_user, name='logout'),
    path('login/', login_user, name='login'),
    path('activate/<uidb64>/<token>', activate, name='activate'),
    
    path('accounts/', include('allauth.urls')),
     
     

    path('product/<str:slug>', product_detail, name = "product"),
    path('product/<str:slug>/add-to-cart', add_to_cart, name = "add-to-cart"),
    path('cart/', cart, name='cart'),
    path('cart/delete', delete_cart, name='delete-cart'),
    
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
