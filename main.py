
#!/usr/bin/python3

from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import subprocess
import shlex
import re


app = Flask(__name__)

host ="https://cpp2latex.pythonanywhere.com/"
app.config["UPLOAD_FOLDER"] = "/home/instructions/dic/static/dic_temp_files/"

@app.route('/')
def upload_file():
    return render_template('index.html')


@app.route('/display', methods = ['GET', 'POST'])
def save_file():
    if request.method == 'POST':
        input_func=request.form['code']

        latex_code = """
        \\usepackage{algorithm}
        \\usepackage{algpseudocode}
        \\begin{algorithm}
        """
        def extract_func_info(input_func):
            func_name = re.search("(\w+)\s*\(", input_func).group(1)
            parameters = re.search("\((.*)\)", input_func).group(1)
            # parameter_list = parameters.split(",")
            # parameter_list = [x.strip() for x in parameter_list]
            return func_name, parameters

        func_name, parameter_list = extract_func_info(input_func)
        # print(func_name)  # Output: "add"
        # print(parameter_list)  # Output: ["int a", "int b"]

        def camel_to_sentence(camel_case_word):
            camel_case_word=camel_case_word[0].upper()+camel_case_word[1:]
            parts = re.findall(r'[A-Z](?:[a-z]+|[A-Z]*(?=[A-Z]|$))', camel_case_word)
            parts = [part.capitalize() for part in parts]
            return ' '.join(parts)

        latex_caption = camel_to_sentence(func_name)

        latex_code += f"\\caption{{{latex_caption}}}\n"

        latex_code += "\\begin{algorithmic}\n"
        latex_code += f"\\Procedure{{{func_name}}}{{{parameter_list}}}\n"

        def add_space(input_func):
             return re.sub(r"([^\w\s=_&|/])(\w|\b)", r"\1 \2", re.sub(r"(\w|\b)([^\w\s=_&|/])", r"\1 \2", input_func))

        input_func = add_space(input_func)

        def replace_comments(input_func):
           return re.sub(r"//", "// ", input_func)
        input_func = replace_comments(input_func)

        def extract_function_body(input_func):
            start = input_func.index("{") + 1
            end = input_func.rindex("}")
            return input_func[start:end]

        function_body = extract_function_body(input_func)

        def add_space(input_func):
             return re.sub(r"(\w)([^\w\s])", r"\1 \2", input_func)

        function_body=add_space(function_body)
# print(input_func)
        latex_code += """\\EndProcedure
        \\end{algorithmic}
        \\end{algorithm}
        """     
        out = latex_code

    return render_template('index.html', output=out)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug = True)
