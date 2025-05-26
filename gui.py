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
        # Get code from form
        code = request.form.get('code', '')
        if not code:
            return render_template('index.html', output='Error: No code provided.', code=code)
        
        # Save code to a temporary .unn file
        temp_file = 'temp_input.unn'
        try:
            with open(temp_file, 'w') as f:
                f.write(code)
            
            # Run the compiler (assumes ./main is the compiled binary)
            compile_result = subprocess.run(['./build/unn', temp_file , "output"], capture_output=True, text=True, timeout=10)
            print(compile_result)
            result = subprocess.run(['./output'], capture_output=True, text=True, timeout=10)
            output = result.stdout or result.stderr or "No output produced."
            print(result)
        except subprocess.TimeoutExpired:
            output = "Error: Compilation timed out."
        except Exception as e:
            output = f"Error: {str(e)}"
        finally:
            # Clean up temporary file
            if os.path.exists(temp_file):
                os.remove(temp_file)
        
        return render_template('index.html', output=output, code=code)
    
    # Handle GET requests to /compile (e.g., direct URL access)
    return render_template('index.html', output='Please submit code using the form.', code='')

if __name__ == '__main__':
    print("Starting Flask server on http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)