from prompt_toolkit.completion import WordCompleter, Completion
from prompt_toolkit.formatted_text import ANSI

class CustomWordCompleter(WordCompleter):
    def get_completions(self, document, complete_event):
        word_before_cursor = document.get_word_before_cursor()
        completions = []

        for word in self.words:
            if word.startswith(word_before_cursor):
                display_text = ANSI('\x1b[34m' + word + '\x1b[0m')  # Adjust the spacing here
                completion = Completion(word, start_position=-len(word_before_cursor), display=display_text)
                completions.append(completion)

        return completions
    