from flask import Flask, render_template, request
import subprocess
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html', output='', code='')

@app.route('/compile', methods=['GET', 'POST'])
def compile():
    if request.method == 'POST':
        code = request.form.get('code', '')
        if not code:
            return render_template('index.html', output='Error: No code provided.', code=code)

        temp_file = 'temp_input.unn'
        try:
            with open(temp_file, 'w') as f:
                f.write(code)

            # Run compiler and capture both stdout and stderr
            compile_result = subprocess.run(
                ['./build/unn', temp_file, 'output'],
                capture_output=True, text=True, timeout=10
            )

            compiler_stdout = compile_result.stdout.strip()
            compiler_stderr = compile_result.stderr.strip()
            compiler_output = compiler_stdout + ("\n" + compiler_stderr if compiler_stderr else "")

            if compile_result.returncode != 0:
                output = f"Compilation Error:\n{compiler_output}"
            else:
                # Run the generated output binary
                run_result = subprocess.run(
                    ['./output'],
                    capture_output=True, text=True, timeout=10
                )

                runtime_stdout = run_result.stdout.strip()
                runtime_stderr = run_result.stderr.strip()
                runtime_output = runtime_stdout + ("\n" + runtime_stderr if runtime_stderr else "")

                # Combine outputs
                output = f"{compiler_output}\n\nProgram Output:\n{runtime_output}".strip()

        except subprocess.TimeoutExpired:
            output = "Error: Compilation or execution timed out."
        except Exception as e:
            output = f"Unexpected Error: {str(e)}"
        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)

        return render_template('index.html', output=output, code=code)

    return render_template('index.html', output='Please submit code using the form.', code='')

if __name__ == '__main__':
    print("Starting Flask server on http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
