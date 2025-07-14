from prompt_toolkit import PromptSession
from prompt_toolkit.shortcuts import CompleteStyle
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.shortcuts import CompleteStyle

class PromptInput:
    def __init__(self):
        self.completer = None
        self.style = None
        self.corrections = None
        self.history = None


        self.bindings = KeyBindings()

        @self.bindings.add(" ")
        def _(event):
            b = event.app.current_buffer
            w = b.document.get_word_before_cursor()

            if w is not None:
                if w in self.corrections:
                    b.delete_before_cursor(count=len(w))
                    b.insert_text(self.corrections[w])

            b.insert_text(" ")

    def add_history_commands_to_completer(self):
        for command in self.history.load_history_strings():
            words = command.split()
            for word in words:
                if word not in self.completer.words:
                    self.completer.words.append(word)

    def get_input(self, prompt_text):
        #self.add_history_commands_to_completer()
        if self.history is not None:
            # Tools
            session = PromptSession(
                history=self.history,
                completer=self.completer,
                complete_style=CompleteStyle.READLINE_LIKE,
                key_bindings=self.bindings,
                style= self.style,
            )
        else:
            # Menu
            session = PromptSession(
                completer=self.completer,
                complete_style=CompleteStyle.READLINE_LIKE,
                style= self.style,
                key_bindings=self.bindings,
            )

        return session.prompt(prompt_text)

    def set_completer(self, completer):
        self.completer = completer

    def set_corrections(self, corretions):
        self.corrections = corretions

    def set_style(self, style):
        self.style = style

    def set_history(self, history):
        self.history = history
