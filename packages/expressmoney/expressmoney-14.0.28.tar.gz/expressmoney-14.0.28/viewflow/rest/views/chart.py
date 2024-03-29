import json
import six

from rest_framework import permissions, views, renderers
from rest_framework.response import Response

from ... import chart
from .mixins import FlowAPIMixin


PERMISSION_DENIED = """<svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%">
  <g transform="translate(50,50)">
    <text x="0" y="0" font-size="35">
      {}
    </text>
  </g>
</svg>
"""


class SVGRenderer(renderers.BaseRenderer):
    media_type = "image/svg+xml"
    format = 'svg'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        if isinstance(data, dict):
            return PERMISSION_DENIED.format(data.get('detail', 'Error'))
        return chart.grid_to_svg(data)


class SVGJSONRenderer(renderers.JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        if isinstance(data, dict):
            result = json.dumps(data, ensure_ascii=True)
            if isinstance(result, six.text_type):
                result = result.replace('\u2028', '\\u2028').replace('\u2029', '\\u2029')
                return bytes(result.encode('utf-8'))
            return result
        data = {'svg': chart.grid_to_svg(data)}
        return super(SVGJSONRenderer, self).render(data, accepted_media_type=None, renderer_context=None)


class FlowChartView(FlowAPIMixin, views.APIView):
    flow_class = None
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = (SVGRenderer, SVGJSONRenderer)

    def get(self, request, *args, **kwargs):
        grid = chart.calc_layout_data(kwargs['flow_class'])
        return Response(grid)
