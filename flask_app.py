from flask import Flask, render_template
import os

app = Flask(__name__)

OUTPUT_FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'zawartosc.txt')

@app.route('/')
def index():
    try:
        with open(OUTPUT_FILE_PATH, 'r') as f:
            output_content = f.read()
    except FileNotFoundError:
        output_content = "Plik outputu gry nie został jeszcze utworzony."
    return render_template('index.html', output_text=output_content)

if __name__ == '__main__':
    app.run(debug=True)