import jinja2
from pdfkit import from_string


# class to load template and render it
class TemplateProcessor:
    def __init__(self, template_file, data):
        self.template_file = template_file
        self.data = data

    def render(self):
        template_env = jinja2.Environment(loader=jinja2.PackageLoader('invoicify', 'templates'))
        template = template_env.get_template(self.template_file)
        return template.render(**self.data)

    def render_to_pdf(self, output_file):
        html = self.render()
        return from_string(html, output_file)
