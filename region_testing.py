import sublime, sublime_plugin

global region_test
region_test = {}


class AddRegionTestCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		global region_test

		for region in self.view.sel():

			region_test['y'] = region
			self.view.add_regions('y', [region], 'comment', 'dot', sublime.HIDE_ON_MINIMAP)

class CheckIfEqualCommand(sublime_plugin.TextCommand):
	def run(self, edit):

		global region_test
		region1 = self.view.get_regions('y')
		print(id(region1[0]))
		print(id(region_test['y'])
