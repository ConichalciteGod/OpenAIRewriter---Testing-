import tkinter as tk
from tkinter import messagebox
import openai
from config import openai_api_key
import datetime


class TextRewriterApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Text Rewriter")

        openai.api_key = openai_api_key

        self.models = {
            "Davinci": "text-davinci-002",
            "Curie": "text-curie-001",
            "Babbage": "text-babbage-001",
            "Ada": "text-ada-001"
        }
        self.model_var = tk.StringVar(value="Davinci")

        self.input_text = tk.Text(self, height=5, width=30)
        self.input_text.pack()

        self.model_dropdown = tk.OptionMenu(self, self.model_var, *self.models.keys())
        self.model_dropdown.pack()

        self.temperature_scale = tk.Scale(self, from_=0.1, to=1.0, resolution=0.1, orient=tk.HORIZONTAL)
        self.temperature_scale.set(0.5)
        self.temperature_scale.pack()

        self.max_tokens_scale = tk.Scale(self, from_=16, to=2048, resolution=16, orient=tk.HORIZONTAL)
        self.max_tokens_scale.set(1024)
        self.max_tokens_scale.pack()

        self.button_frame = tk.Frame(self)
        self.button_frame.pack()

        self.rewrite_button = tk.Button(self.button_frame, text="Rewrite", command=self.update_text)
        self.rewrite_button.pack(side=tk.LEFT)

        self.copy_button = tk.Button(self.button_frame, text="Copy", command=self.copy_text)
        self.copy_button.pack(side=tk.LEFT)

        self.output_text = tk.Text(self, height=5, width=30)
        self.output_text.pack()

        self.processing_time = tk.Label(self, text="")
        self.processing_time.pack()

    def rewrite_text(self, text, model, temperature, max_tokens):
        prompt = f"Rewrite the text: {text}"
        start_time = datetime.datetime.now()
        try:
            response = openai.Completion.create(
                engine=self.models[model],
                prompt=prompt,
                max_tokens=max_tokens,
                n=1,
                stop=None,
                temperature=temperature,
                presence_penalty=0.5,
                frequency_penalty=0.5,
                best_of=1
            )
        except openai.Error as e:
            messagebox.showerror("Error", str(e))
            return "", 0
        rewritten_text = response.choices[0].text.strip()
        end_time = datetime.datetime.now()
        time_taken = (end_time - start_time).total_seconds()
        return rewritten_text, time_taken

    def update_text(self):
        text, time = self.rewrite_text(self.input_text.get("1.0", "end"), self.model_var.get(), self.temperature_scale.get(), self.max_tokens_scale.get())
        self.output_text.delete("1.0", "end")
        self.output_text.insert("1.0", text)
        self.processing_time.config(text=f"Processing Time: {time:.2f} seconds")
        pass

    def copy_text(self):
        self.clipboard_clear()
        self.clipboard_append(self.output_text.get("1.0", "end"))


if __name__ == "__main__":
    app = TextRewriterApp()
    app.mainloop()
