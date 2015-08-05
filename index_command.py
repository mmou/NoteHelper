import sublime, sublime_plugin, os, string
import os, io, string, logging
from gensim import corpora, models, similarities

class IndexCommand(sublime_plugin.TextCommand):

    def run(self, edit):   
        self.this_window = sublime.active_window()

        results = "hi"
        self.this_window.new_file().insert(edit, 0, str(results))
    