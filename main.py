from flask import Flask, render_template, request

app = Flask(__name__)

def convert_code(source_lang, target_lang, source_code):
    if source_lang == target_lang:
        return source_code

    lines = source_code.strip().split('\n')
    converted = []

    for line in lines:
        line = line.strip()

        # ---------- Python to Java ----------
        if source_lang == "python" and target_lang == "java":
            if line.startswith("print("):
                content = line[6:-1]
                converted.append(f'System.out.println({content});')
            elif line.startswith("for ") and " in range(" in line:
                var = line.split("for ")[1].split(" in")[0].strip()
                range_val = line.split("range(")[1].rstrip("):")
                converted.append(f'for (int {var} = 0; {var} < {range_val}; {var}++) {{')
            elif line.startswith("if "):
                condition = line[3:].rstrip(":")
                converted.append(f'if ({condition}) {{')
            elif line.startswith("def "):
                name = line[4:].split("(")[0]
                args = line[line.find("(")+1:line.find(")")]
                converted.append(f'public static void {name}({args}) {{')
            elif line.endswith(":"):
                converted.append("// Converted block starts")
            elif line == "":
                continue
            else:
                converted.append(f'    {line}')
            if line.endswith(":"):
                converted.append("}")

        # ---------- Java to Python ----------
        elif source_lang == "java" and target_lang == "python":
            if line.startswith("System.out.println("):
                content = line[19:-2]
                converted.append(f'print({content})')
            elif line.startswith("for (int ") and ";" in line:
                parts = line.replace("for (", "").replace(")", "").replace("int ", "").split(";")
                var = parts[0].split("=")[0].strip()
                end = parts[1].split("<")[1].strip()
                converted.append(f'for {var} in range({end}):')
            elif line.startswith("if (") and line.endswith(") {"):
                condition = line[3:-2]
                converted.append(f'if {condition}:')
            elif "void" in line and "(" in line and ")" in line:
                name = line.split("void")[1].split("(")[0].strip()
                args = line[line.find("(")+1:line.find(")")]
                converted.append(f'def {name}({args}):')
            elif line in ["{", "}"]:
                continue
            elif line.endswith(";"):
                converted.append(f'# {line}')
            else:
                converted.append(line)

        # ---------- JavaScript to Python ----------
        elif source_lang == "javascript" and target_lang == "python":
            if line.startswith("console.log("):
                converted.append(f'print({line[12:-2]})')
            elif line.startswith("function "):
                name = line.split("function ")[1].split("(")[0]
                args = line[line.find("(")+1:line.find(")")]
                converted.append(f'def {name}({args}):')
            elif line.startswith("if ("):
                condition = line[3:line.find(")")]
                converted.append(f'if {condition}:')
            else:
                converted.append(f'# Unconverted: {line}')

        # ---------- C# to Python ----------
        elif source_lang == "csharp" and target_lang == "python":
            if "Console.WriteLine" in line:
                content = line[line.find("(")+1:line.find(")")]
                converted.append(f'print({content})')
            elif line.strip().startswith("for (int "):
                converted.append(f'# Converted loop from C#: {line}')
            elif line.strip().startswith("if ("):
                condition = line[3:line.find(")")]
                converted.append(f'if {condition}:')
            elif line.startswith("public void"):
                name = line.split("void")[1].split("(")[0].strip()
                args = line[line.find("(")+1:line.find(")")]
                converted.append(f'def {name}({args}):')
            else:
                converted.append(f'# Unconverted: {line}')
        else:
            converted.append(f"# Cannot convert line: {line}")

    return "\n".join(converted)

@app.route("/", methods=["GET", "POST"])
def index():
    converted_code = ""
    if request.method == "POST":
        source_lang = request.form.get("source_language")
        target_lang = request.form.get("target_language")
        source_code = request.form.get("source_code")
        converted_code = convert_code(source_lang, target_lang, source_code)
    return render_template("index.html", converted_code=converted_code)

if __name__ == "__main__":
    app.run(debug=True)
