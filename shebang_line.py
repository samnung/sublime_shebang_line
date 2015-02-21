#!/usr/bin/env python

import sublime, sublime_plugin

class Language:
	def __init__(self, name, shebang_line = None):
		self.name = name
		self.shebang_line = shebang_line

		if shebang_line == None:
			self.shebang_line = '/usr/bin/env %s' % name.lower()


LANGUAGES = [
	Language('Python'),
	Language('Bash'),
	Language('Ruby', '/usr/bin/ruby'),
]

LANGUAGES_NAMES = list(map(lambda lang: lang.name, LANGUAGES))


class ShebangLineAddCommand(sublime_plugin.TextCommand):
	def on_click(self, index):
		if index >= 0:
			lang = LANGUAGES[index]
			formatted_shebang = '#!%s\n' % lang.shebang_line
			self.view.run_command('shebang_line_add_finish', {'shebang_line': formatted_shebang})

	def run(self, edit):
		sublime.active_window().show_quick_panel(LANGUAGES_NAMES, self.on_click)


class ShebangLineAddFinishCommand(sublime_plugin.TextCommand):
	def run(self, edit, shebang_line):
		region = self.view.find('#!.*\n?', 0)
		
		if region.a == -1:
			self.view.insert(edit, 0, shebang_line)
		else:
			self.view.replace(edit, region, shebang_line)
