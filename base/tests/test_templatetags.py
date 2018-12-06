from django.template import Context, Template


class TestTemplateTags:
	"""test for template tags"""
	def test_concat_tag(self):
		tpl = Template("{% load ttags %}{{ 'two'|_concat:'words' }}")
		rendered = tpl.render(Context({}))

		assert 'two words' == rendered

