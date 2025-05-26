from flask import Flask, render_template, request
import subprocess
import os

app = Flask(__name__)

def run_binary():
    # Run the generated binary and capture output reliably
    process = subprocess.Popen(["./output"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = process.communicate()

    output = stdout.strip()
    if stderr:
        output += "\n[stderr]\n" + stderr.strip()
    return output

@app.route('/', methods=['GET', 'POST'])
def index():
    output = ""
    code = ""

    if request.method == 'POST':
        code = request.form['code']

        # Save the input code
        with open('temp_input.unn', 'w') as f:
            f.write(code)

        try:
            # Step 1: Build your compiler
            subprocess.run(["bash", "build.sh"], check=True)

            # Step 2: Run the compiler on input file
            subprocess.run(["./build/unn", "temp_input.unn", "output"], check=True)

            # Step 3: Run the compiled binary and capture its output
            output = run_binary()

        except subprocess.CalledProcessError as e:
            output = f"Error occurred:\n{e}"

    return render_template('index.html', output=output, code=code)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
