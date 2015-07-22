import sublime, sublime_plugin, os, string

IGNORE_FILENAMES = set([".Ulysses-Group.plist"])
ACCEPT_FILETYPES = set([".txt", ".md"])

STOP_WORDS = set(["a", "about", "above", "above", "across", "after", "afterwards", 
    "again", "against", "all", "almost", "alone", "along", "already", "also","although",
    "always","am","among", "amongst", "amoungst", "amount",  "an", "and", "another", 
    "any","anyhow","anyone","anything","anyway", "anywhere", "are", "around", "as",  
    "at", "back","be","became", "because","become","becomes", "becoming", "been", "before", 
    "beforehand", "behind", "being", "below", "beside", "besides", "between", "beyond", 
    "bill", "both", "bottom","but", "by", "call", "can", "cannot", "cant", "co", "con", 
    "could", "couldnt", "cry", "de", "describe", "detail", "do", "done", "down", "due", 
    "during", "each", "eg", "eight", "either", "eleven","else", "elsewhere", "empty", 
    "enough", "etc", "even", "ever", "every", "everyone", "everything", "everywhere", 
    "except", "few", "fifteen", "fify", "fill", "find", "fire", "first", "five", "for", 
    "former", "formerly", "forty", "found", "four", "from", "front", "full", "further", 
    "get", "give", "go", "had", "has", "hasnt", "have", "he", "hence", "her", "here", 
    "hereafter", "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", 
    "his", "how", "however", "hundred", "ie", "if", "in", "inc", "indeed", "interest", 
    "into", "is", "it", "its", "itself", "keep", "last", "latter", "latterly", "least", 
    "less", "ltd", "made", "many", "may", "me", "meanwhile", "might", "mill", "mine", 
    "more", "moreover", "most", "mostly", "move", "much", "must", "my", "myself", "name", 
    "namely", "neither", "never", "nevertheless", "next", "nine", "no", "nobody", "none", 
    "noone", "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on", "once", 
    "one", "only", "onto", "or", "other", "others", "otherwise", "our", "ours", "ourselves", 
    "out", "over", "own","part", "per", "perhaps", "please", "put", "rather", "re", "same", 
    "see", "seem", "seemed", "seeming", "seems", "serious", "several", "she", "should", 
    "show", "side", "since", "sincere", "six", "sixty", "so", "some", "somehow", "someone", 
    "something", "sometime", "sometimes", "somewhere", "still", "such", "system", "take", 
    "ten", "than", "that", "the", "their", "them", "themselves", "then", "thence", "there", 
    "thereafter", "thereby", "therefore", "therein", "thereupon", "these", "they", "thickv", 
    "thin", "third", "this", "those", "though", "three", "through", "throughout", "thru", 
    "thus", "to", "together", "too", "top", "toward", "towards", "twelve", "twenty", "two", 
    "un", "under", "until", "up", "upon", "us", "very", "via", "was", "we", "well", "were", 
    "what", "whatever", "when", "whence", "whenever", "where", "whereafter", "whereas", 
    "whereby", "wherein", "whereupon", "wherever", "whether", "which", "while", "whither", 
    "who", "whoever", "whole", "whom", "whose", "why", "will", "with", "within", "without", 
    "would", "yet", "you", "your", "yours", "yourself", "yourselves", "the"])

MY_STOP_WORDS = set(["i", "i'm"])

class StatsCommand(sublime_plugin.TextCommand):
    def run(self, edit):

        self.words = {}
        self.this_window = sublime.active_window()

        self.traverse(edit)

        self.this_window.new_file().insert(edit, 0, str(self.words))

    def traverse(self, edit):
        folders = self.this_window.folders()
        for folder in folders:
            for (dirpath, dirnames, filenames) in os.walk(folder):
                for f in filenames:
                    for af in ACCEPT_FILETYPES:
                        if f.endswith(af) and f not in IGNORE_FILENAMES:
                            self.count_words(os.path.join(dirpath, f))

    def count_words(self, path):
        with open(path, mode="r", encoding="utf-8") as f:
            for line in f:
                for word in line.split():
                    clean_word = word.lower().strip(string.punctuation)
                    if clean_word != "" and clean_word not in STOP_WORDS and clean_word not in MY_STOP_WORDS:
                        if clean_word in self.words:
                            self.words[clean_word] += 1
                        else:
                            self.words[clean_word] = 1