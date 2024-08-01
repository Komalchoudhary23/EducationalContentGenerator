from boltiotai import openai
import os
from flask import Flask, render_template_string, request

# Set the OpenAI API key from environment variable
openai.api_key = os.environ['OPENAI_API_KEY']

# Define the function to generate educational content using OpenAI API
def generate_educational_content(course_title):
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful educational assistant."},
                {
                    "role": "user",
                    "content": f"Generate educational content for the course titled '{course_title}'. "
                               "1. Objective of the Course: "
                               "2. Sample Syllabus: "
                               "3. Three Measurable Outcomes (Knowledge, Comprehension, Application): "
                               "4. Assessment Methods: "
                               "5. Recommended Readings and Textbooks: "
                }
            ]
        )
        print(response)
        return response['choices'][0]['message']['content']
    
# Create the Flask app
app = Flask(__name__)

# Define the main route
@app.route('/', methods=['GET', 'POST'])
def index():
    output = ""
    if request.method == 'POST':
        course_title = request.form['course_title']
        output = generate_educational_content(course_title)
        
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Educational Content Generator</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
            <script>
                async function generateContent() {
                    const course_title = document.querySelector('#course_title').value;
                    const output = document.querySelector('#output');
                    output.textContent = 'Generating educational content for you...';
                    const response = await fetch('/generate', {
                        method: 'POST',
                        body: new FormData(document.querySelector('#content-form'))
                    });
                    const newOutput = await response.text();
                    output.innerHTML = newOutput;
                }
                function copyToClipboard() {
                    const output = document.querySelector('#output');
                    const textarea = document.createElement('textarea');
                    textarea.value = output.textContent;
                    document.body.appendChild(textarea);
                    textarea.select();
                    document.execCommand('copy');
                    document.body.removeChild(textarea);
                    alert('Copied to clipboard');
                }
            </script>
        </head>
        <body>
            <div class="container">
                <h1 class="my-4">Educational Content Generator</h1>
                <form id="content-form" onsubmit="event.preventDefault(); generateContent();" class="mb-3">
                    <div class="mb-3">
                        <label for="course_title" class="form-label">Course Title:</label>
                        <input type="text" class="form-control" id="course_title" name="course_title" placeholder="Enter the course title" required>
                    </div>
                    <button type="submit" class="btn btn-primary">Generate Content</button>
                </form>
                <div class="card">
                    <div class="card-header d-flex justify-content-between align-items-center">
                        Output:
                        <button class="btn btn-secondary btn-sm" onclick="copyToClipboard()">Copy</button>
                    </div>
                    <div class="card-body">
                        <pre id="output" class="mb-0" style="white-space: pre-wrap;">{{ output }}</pre>
                    </div>
                </div>
            </div>
        </body>
        </html>
    ''',
                                  output=output)

# Define the generate route
@app.route('/generate', methods=['POST'])
def generate():
    course_title = request.form['course_title']
    return generate_educational_content(course_title)

# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
