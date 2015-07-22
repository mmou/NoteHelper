import sublime, sublime_plugin, urllib, requests

def title_case(string):
    no_caps = set(["a", "an", "the", "at", "by", "for", "in", 
        "of", "on", "to", "up", "and", "as", "but", "or", "nor"])
    words = string.lower().split(" ")
    cased_words = [(word[0].upper() + word[1:]) if (word not in no_caps) else word for word in words]
    return " ".join(cased_words)

def format_result(search_result):
    lines = search_result.split("\n")
    formatted_lines = [("> " + line) for line in lines]
    return "\n".join(formatted_lines) + "\n"

def search_wiki(search_string):
    try:
        clean_search_string = search_string.rstrip("\n").strip()
        safe_search_string = urllib.parse.quote(title_case(clean_search_string),safe='') 
        url = "https://en.wikipedia.org/w/api.php?action=query&format=json&redirects&prop=extracts&format=json&exsentences=5exintro=&explaintext=&titles=" + safe_search_string
        r = requests.get(url)
        pages = r.json()["query"]["pages"]
        pageid = next(iter(pages))
        extract = pages[pageid]["extract"]
    except:
        return "[]"
    else:
        return extract

class WikiCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.path = sublime.active_window().active_view().file_name()
        results = self.get_results()
        sublime.active_window().new_file().insert(edit, 0, str(results))

    def get_results(self):
        with open(self.path, mode="r+", encoding="utf-8") as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                if line[0:2] == "//":
                    search_string = line[2:]
                    search_result = search_wiki(search_string)
                    lines.insert(i+1, format_result(search_result))
        return "".join(lines)
