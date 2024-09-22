from flask import Flask, render_template, request, session

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Set a secret key for session management

# Sample Quiz Data
quiz_data = [
    {
        "question": "What method do you primarily use to track your finances?",
        "options": ["Spreadsheet", "Financial App", "Paper and pen", "I don't track"]
    },
    {
        "question": "How do you categorize your expenses?",
        "options": ["Essential vs discretionary", "Fixed vs variable", "Monthly vs annual", "I don't categorize"]
    },
    {
        "question": "How do you decide on your financial goals?",
        "options": ["Books or articles", "Financial Advisors", "Online courses or webinars", "Social Media"]
    },
    {
        "question": "What is your primary source of financial information?",
        "options": ["Based on short term needs", "Long term aspirations", "Advice from others", "I don't set goals"]
    },
    {
        "question": "How do you handle unexpected expenses?",
        "options": ["Use savings", "Adjust my budget", "Put it on credit", "Ignore it"]
    },
    {
        "question": "What helps you stick to your budget?",
        "options": ["Accountability partner", "Regular reviews", "Rewards for sticking to it", "I struggle to stay on budget"]
    },
    {
        "question": "What motivates you to save?",
        "options": ["Future investments", "Emergency situations", "Major purchases (e.g. house, car)", "I don't find saving motivating"]
    },
    {
        "question": "How do you keep your savings on track?",
        "options": ["Automated transfers", "Manual deposits", "Saving challenges", "I don't have a strategy"]
    },
    {
        "question": "How do you feel about your current debt level?",
        "options": ["Very comfortable", "Somewhat comfortable", "Uncomfortable", "Overwhelmed"]
    },
    {
        "question": "Have you ever sought professional help for debt management?",
        "options": ["Yes regularly", "Yes, once", "No, but I consider it", "No, I manage it on my own"]
    },
    {
        "question": "What percentage of your income do you aim to save each month?",
        "options": ["31% or more", "21-30%", "11-20%", "0-10%"]
    },
    {
        "question": "What strategy do you use to manage your debt?",
        "options": ["I don't have debt", "Avalanche method", "Debt consolidation", "I dont know"]
    },
    {
        "question": "Which debt do you prioritize paying off first?",
        "options": ["Highest interest rate", "Smallest balance", "Oldest debt", "I don't prioritize"]
    },
    {
        "question": "How often do you review your budget?",
        "options": ["Weekly", "Monthly", "Quarterly", "Rarely or never"]
    },
    {
        "question": "What budgeting method do you follow?",
        "options": ["Zero-based budgeting", "50/30/20 rule", "Envelope system", "I don't have a method"]
    }
]


@app.route('/')
def index():
    session.clear()  # Clear the session on starting a new quiz
    return render_template('quiz.html', question_data=quiz_data[0], question_number=1, total_questions=len(quiz_data))

@app.route('/next/<int:question_index>', methods=['POST'])
def next_question(question_index):
    selected_option = request.form.get('answer')  # Get the selected answer
    if selected_option:
        session[f'option_{question_index}'] = selected_option  # Store the selected option in the session

    if question_index + 1 < len(quiz_data):
        return render_template('quiz.html', question_data=quiz_data[question_index + 1], question_number=question_index + 2, total_questions=len(quiz_data))
    else:
        # Calculate feedback based on selected options
        feedback_score = calculate_feedback(session)
        return render_template('result.html', score=feedback_score, total=len(quiz_data))

def calculate_feedback(session):
    # Count how many times each option is selected
    option_counts = {}
    for key in session.keys():
        selected_option = session[key]
        option_counts[selected_option] = option_counts.get(selected_option, 0) + 1

    # Determine the highest count
    max_count = max(option_counts.values())
    most_selected_option = [key for key, count in option_counts.items() if count == max_count]

    # Assign scores based on most selected option
    if most_selected_option and most_selected_option[0] == quiz_data[0]['options'][0]:
        return "90/100"
    elif most_selected_option and most_selected_option[0] == quiz_data[0]['options'][1]:
        return "80/100"
    elif most_selected_option and most_selected_option[0] == quiz_data[0]['options'][2]:
        return "70/100"
    else:
        return "60/100"

if __name__ == "__main__":
    app.run(debug=True, port=5008)
