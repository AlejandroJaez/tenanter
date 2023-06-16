from django.core.exceptions import DisallowedHost
from django.http import Http404
from django.shortcuts import redirect
from django.urls import resolve
from django.utils.deprecation import MiddlewareMixin
from django_tenants.utils import remove_www, get_tenant_domain_model, get_public_schema_name


from easy_tenants import tenant_context, tenant_context_disabled

from config import settings
from core.models import Tenant

URLS = ["customer-list", "set-tenant"]


class TenantMiddleware(MiddlewareMixin):
    TENANT_NOT_FOUND_EXCEPTION = Http404

    @staticmethod
    def hostname_from_request(request):
        """ Extracts hostname from request. Used for custom requests filtering.
            By default removes the request's port and common prefixes.
        """
        return remove_www(request.get_host().split(':')[0])

    def get_tenant(self, request):
        """Get tenant saved in session request"""
        try:
            hostname = self.hostname_from_request(request)
        except DisallowedHost:
            from django.http import HttpResponseNotFound
            return HttpResponseNotFound()
        domain_model = get_tenant_domain_model()
        try:
            domain = domain_model.objects.select_related('tenant').get(domain=hostname)
        except domain_model.DoesNotExist:
            self.no_tenant_found(request, hostname)
            return
        return domain.tenant

    def process_request(self, request):
        if request.path.startswith("/admin/"):
            with tenant_context_disabled():
                return self.get_response(request)
        tenant = self.get_tenant(request)
        self.tenant = tenant
        request.tenant = tenant
        self.setup_url_routing(request)
        # tenant filter is disabled in admin


        # ignored_path = any(
        #     resolve(request.path).view_name == url for url in URLS
        # )

        if tenant:
            # views works with tenant
            with tenant_context(tenant):
                return self.get_response(request)

    def no_tenant_found(self, request, hostname):
        """ What should happen if no tenant is found.
        This makes it easier if you want to override the default behavior """
        if hasattr(settings, 'SHOW_PUBLIC_IF_NO_TENANT_FOUND') and settings.SHOW_PUBLIC_IF_NO_TENANT_FOUND:
            self.setup_url_routing(request=request, force_public=True)
        else:
            raise self.TENANT_NOT_FOUND_EXCEPTION('No tenant for hostname "%s"' % hostname)

    @staticmethod
    def setup_url_routing(request, force_public=False):
        """
        Sets the correct url conf based on the tenant
        :param request:
        :param force_public
        """
        public_schema_name = get_public_schema_name()

        if (hasattr(settings, 'PUBLIC_SCHEMA_URLCONF') and
                (force_public or request.tenant.name == get_public_schema_name())):
            request.urlconf = settings.PUBLIC_SCHEMA_URLCONF
