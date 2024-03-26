import logging

from lona.responses import TemplateResponse
from lona.view import View

logger = logging.getLogger('lona.views')


class FallbackView(View):
    VIEW_SETTING = ''
    TEMPLATE_SETTING = ''

    def render_default_template(self, request, **extra_context):
        template_setting = request.server.settings.get(self.TEMPLATE_SETTING)

        return TemplateResponse(
            name=template_setting,
            context={
                'request': request,
                **extra_context,
            },
        )

    def handle_request(self, request, **extra_context):
        view_setting = request.server.settings.get(self.VIEW_SETTING, '')

        if view_setting:
            try:
                view_class = request.server._view_loader.load(view_setting)

                view = view_class(
                    server=self.server,
                    view_runtime=self._view_runtime,
                    request=request,
                )

                return view.handle_request(request, **extra_context)

            except Exception:
                logger.exception(
                    "exception raised while running '%s'. running fallback view",
                    view_setting,
                )

                return self.render_default_template(request, **extra_context)

        return self.render_default_template(request, **extra_context)


class FrontendView(FallbackView):
    VIEW_SETTING = 'FRONTEND_VIEW'
    TEMPLATE_SETTING = 'FRONTEND_TEMPLATE'


class Error403View(FallbackView):
    VIEW_SETTING = 'ERROR_403_VIEW'
    TEMPLATE_SETTING = 'ERROR_403_TEMPLATE'


class Error404View(FallbackView):
    VIEW_SETTING = 'ERROR_404_VIEW'
    TEMPLATE_SETTING = 'ERROR_404_TEMPLATE'


class Error500View(FallbackView):
    VIEW_SETTING = 'ERROR_500_VIEW'
    TEMPLATE_SETTING = 'ERROR_500_TEMPLATE'
