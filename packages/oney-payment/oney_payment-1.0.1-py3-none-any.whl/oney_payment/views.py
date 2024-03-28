from django.conf import settings
from django.forms import formset_factory
from django.template.response import TemplateResponse
from django.views.generic import View

from oney_payment.commerce.checkout import CheckoutService
from oney_payment.forms import OrderForm, AddressForm


class OneyExtensionRedirectView(View):
    checkout_service = CheckoutService()

    def get(self, request):
        context = self.checkout_service.get_oney_context(request)

        OrderFormSet = formset_factory(OrderForm, extra=0)
        address_form = AddressForm(initial=context["address"])
        order_formset = OrderFormSet(initial=context["orders"])

        return TemplateResponse(
            request=request,
            template="oney-extension-redirect-form.html",
            context={
                "action_url": settings.ONEY_EXTENSION_URL,
                "action_method": "POST",
                "address_form": address_form,
                "order_formset": order_formset,
            }
        )
