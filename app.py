from flask import Flask, render_template, request

app = Flask(__name__)

# Example puzzles and questions
locations = ["Dunkin donuts", "Library", "Frisco", "Orange Team", "Geeta"]

# Solver 1 data with associated passwords for Solver 2
solver1_data = {
    "flaggergasted": {
        "question": "Buffer Overflow: What is a common cause of buffer overflow in C programs?\n"
                    "a) Using malloc for memory allocation\n"
                    "b) Using strcpy without checking the size of the destination buffer\n"
                    "c) Using strlen to get string length\n"
                    "d) Using sizeof to calculate memory size\n",
        "answer": "b",
        "next_solver2_password": "hackbar"
    },
    "captured": {
        "question": "Dynamic Memory: What happens if you delete a pointer in C++ but try to access it afterward?\n"
                    "a) The program will crash immediately\n"
                    "b) It may cause undefined behavior\n"
                    "c) The pointer will automatically reset to null\n"
                    "d) Nothing happens\n",
        "answer": "b",
        "next_solver2_password": "rooted"
    },
    "marked": {
        "question": "Secure Hashing: Which of the following is used to hash a password securely in C++?\n"
                    "a) std::hash\n"
                    "b) md5\n"
                    "c) getpass\n"
                    "d) None of the above\n",
        "answer": "a",
        "next_solver2_password": "breachit"
    },
    "mayonaise": {
        "question": "SQL Injection: What is the best way to prevent SQL injection in Python?\n"
                    "a) Use eval() to sanitize inputs\n"
                    "b) Use parameterized queries\n"
                    "c) Validate inputs with regex\n"
                    "d) Use dynamic queries\n",
        "answer": "b",
        "next_solver2_password": "scriptkiddie"
    },
    "laughtop": {
        "question": "Password Hashing: Which Python module is commonly used for hashing passwords?\n"
                    "a) os\n"
                    "b) hashlib\n"
                    "c) pickle\n"
                    "d) getpass\n",
        "answer": "b",
        "next_solver2_password": "firewalllol"
    }
}

# Solver 2 questions
solver2_data = {
    "unlock1": {
        "question": "Cross-Site Scripting (XSS): Which of the following techniques prevents XSS attacks in a Python web application?\n"
                    "a) Use eval() to filter inputs\n"
                    "b) Sanitize user input with HTML escaping\n"
                    "c) Disable cookies in the browser\n"
                    "d) Use dynamic HTML templates\n",
        "answer": "b",
        "next_solver2_password": "unlock2"
    },
    "unlock2": {
        "question": "File Handling: In Python, which mode allows reading and writing to a file without overwriting its contents?\n"
                    "a) \"w+\"\n"
                    "b) \"r+\"\n"
                    "c) \"a+\"\n"
                    "d) \"x+\"\n",
        "answer": "c",
        "next_solver2_password": "unlock3"
    },
    "unlock3": {
        "question": "Input Validation: Which function is safer for reading strings in C to prevent buffer overflow?\n"
                    "a) gets()\n"
                    "b) scanf()\n"
                    "c) strncpy()\n"
                    "d) printf()\n",
        "answer": "c",
        "next_solver2_password": "unlock4"
    },
    "unlock4": {
        "question": "File Access: What mode should be used to open a file in C for writing, where data should be appended at the end of the file?\n"
                    "a) \"w\"\n"
                    "b) \"a\"\n"
                    "c) \"r+\"\n"
                    "d) \"wb\"\n",
        "answer": "b",
        "next_solver2_password": "unlock5"
    },
    "unlock5": {
        "question": "Exception Handling: Which keyword is used to handle exceptions in C++?\n"
                    "a) catch\n"
                    "b) try\n"
                    "c) throw\n"
                    "d) All of the above\n",
        "answer": "d",
        "next_solver2_password": None
    }
}

# Application state variables
current_location_index = 0
solver1_password = None
solver2_password = None
finder_password = "start"  # Initial password for the Finder


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/finder", methods=["GET", "POST"])
def finder():
    global current_location_index, solver1_password
    if request.method == "POST":
        password = request.form.get("finder_password")
        if password == "start" or password == solver2_password:
            location = locations[current_location_index]
            solver1_password = list(solver1_data.keys())[current_location_index]
            current_location_index += 1
            if current_location_index >= len(locations):
                return "Congratulations! All locations completed!"
            return f"Go to the next location: {location}"
        return "Incorrect password. Try again."
    return render_template("finder.html")


@app.route("/solver1", methods=["GET", "POST"])
def solver1():
    global solver1_password
    if request.method == "POST":
        entered_password = request.form.get("solver_password")
        if entered_password in solver1_data:
            solver1_password = entered_password
            question = solver1_data[solver1_password]["question"]
            return render_template("solver1.html", status="unlocked", question=question, current_password=solver1_password)
        return render_template("solver1.html", status="locked", error="Incorrect password.")
    return render_template("solver1.html", status="locked")


@app.route("/submit_solver1", methods=["POST"])
def submit_solver1():
    global solver2_password
    current_password = request.form.get("current_password")
    answer = request.form.get("answer").strip().lower()

    if current_password in solver1_data and answer == solver1_data[current_password]["answer"]:
        solver2_password = solver1_data[current_password]["next_solver2_password"]
        return render_template(
            "solver1.html",
            status="unlocked",
            question=solver1_data[current_password]["question"],
            current_password=current_password,
            message=f"Correct! Password for Solver 2 is now unlocked: {solver2_password}",
        )
    return render_template(
        "solver1.html",
        status="unlocked",
        question=solver1_data[current_password]["question"],
        current_password=current_password,
        error="Incorrect answer. Try again."
    )


@app.route("/solver2", methods=["GET", "POST"])
def solver2():
    global solver2_password, current_location_index
    if request.method == "POST":
        entered_password = request.form.get("solver_password")
        if entered_password == solver2_password:
            question = solver2_data.get(solver2_password, {}).get("question")
            return render_template(
                "solver2.html",
                question=question,
                status="unlocked",
                current_password=solver2_password
            )
        return render_template("solver2.html", status="locked", error="Incorrect password.")
    return render_template("solver2.html", status="locked")


@app.route("/submit_solver2", methods=["POST"])
def submit_solver2():
    global solver2_password, current_location_index
    current_password = request.form.get("current_password")
    answer = request.form.get("answer").strip().lower()

    if current_password in solver2_data and answer == solver2_data[current_password]["answer"]:
        next_password = solver2_data[current_password]["next_solver2_password"]
        solver2_password = next_password if next_password else solver2_password

        if current_location_index < len(locations):
            location = locations[current_location_index]
            current_location_index += 1
            return render_template(
                "solver2.html",
                status="unlocked",
                question=solver2_data[current_password]["question"],
                current_password=current_password,
                message=f"Correct! Go to the next location: {location}"
            )
        else:
            return render_template(
                "solver2.html",
                status="unlocked",
                question=solver2_data[current_password]["question"],
                current_password=current_password,
                message="Congratulations! You have completed all locations!"
            )
    return render_template(
        "solver2.html",
        status="unlocked",
        question=solver2_data[current_password]["question"],
        current_password=current_password,
        error="Incorrect answer. Try again."
    )


if __name__ == "__main__":
    app.run(debug=True)
