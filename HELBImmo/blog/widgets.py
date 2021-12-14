from django import forms
from django.template import loader
from django.utils.safestring import mark_safe

class MapWidget(forms.widgets.Widget):
    template_name = 'blog/widgets/map_widget.html'

    class Media:
        css = {'all': (
            "https://cdn.jsdelivr.net/npm/ol-geocoder@latest/dist/ol-geocoder.min.css",
            "https://cdn.jsdelivr.net/gh/openlayers/openlayers.github.io@master/en/v6.9.0/css/ol.css" )}
        js = ("https://cdn.jsdelivr.net/gh/openlayers/openlayers.github.io@master/en/v6.9.0/build/ol.js",
        "https://cdn.jsdelivr.net/npm/ol-geocoder",
        "blog/mapWidget.js")

    def render(self, name, value, attrs=None, renderer=None):

        context = self.get_context(name, value, attrs)

        if renderer != None:
            output = renderer.render(self.template_name, context)
        else:
            output = loader.get_template(self.template_name).render(context)
        return mark_safe(output)
    