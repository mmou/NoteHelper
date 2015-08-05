import sublime, sublime_plugin, os, string, math
from NoteHelper import const

class Stats2Command(sublime_plugin.TextCommand):
    def run(self, edit):
        self.documents = {}
        self.documents_scored = {}
        self.terms = {}
        self.terms_scored = {}        
        self.this_window = sublime.active_window()
        self.traverse()     # populate self.documents with raw counts
        self.tf_idf()       # tf-idf

        results = self.terms_scored
        self.this_window.new_file().insert(edit, 0, str(results))

    def traverse(self):
        folders = self.this_window.folders()
        for folder in folders:
            for (dirpath, dirnames, filenames) in os.walk(folder):
                for f in filenames:
                    for af in const.ACCEPT_FILETYPES:
                        if f.endswith(af) and f not in const.IGNORE_FILENAMES:
                            self.populate_dicts(os.path.join(dirpath, f))

    def populate_dicts(self, path):
        with open(path, mode="r", encoding="utf-8") as f:
            term_freqs = {}
            for line in f:
                for word in line.split():
                    clean_word = word.lower().strip(string.punctuation)
                    if clean_word != "" and clean_word not in const.STOP_WORDS and clean_word not in const.MY_STOP_WORDS:
                        if clean_word in term_freqs:
                            term_freqs[clean_word] += 1
                        else:
                            term_freqs[clean_word] = 1                            
                            if clean_word in self.terms:
                                self.terms[clean_word] += 1
                            else:
                                self.terms[clean_word] = 1
            self.documents[path] = term_freqs

    def tf_idf(self):
        num_docs = len(self.documents)
        for doc in self.documents:
            self.documents_scored[doc] = {}
            num_terms = len(self.documents[doc])
            for term in self.documents[doc]:
#                tf = self.documents[doc][term]/num_terms
                tf = 1+math.log(self.documents[doc][term], 10)
                idf = math.log(num_docs/self.terms[term], 10)
                tf_idf = round(tf*idf, 5)
                self.documents_scored[doc][term] = tf_idf

                if term in self.terms_scored:                       
                    self.terms_scored[term] += tf_idf
                else:
                    self.terms_scored[term] = tf_idf

            self.documents_scored[doc] = dict(sorted(self.documents[doc].items(), key=lambda e:e[1], reverse=True)[:5])
