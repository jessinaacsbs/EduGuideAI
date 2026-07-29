from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from groq import Groq
import os
import re

load_dotenv()

app = Flask(__name__)


client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


SYSTEM_PROMPT = """
You are EduGuide AI, a personal AI tutor.

Rules:
- Detect language.
- Detect subject.
- Detect student level.
- Teach concept before answer.
- Give simple step-by-step explanation.
- Give real life example.
- Give key takeaway.
- Give ONE practice question.
- Do not encourage cheating.
- Do not invent information.

Return ONLY this format:

CONCEPT:
(write explanation)

STEPS:
(write steps)

EXAMPLE:
(write one real-life example)

FLOWCHART:

(Write ONLY one step per line.

Do NOT use numbers.

Do NOT use bullets.

Do NOT use arrows.

Example:

Start

Find middle element

Compare with target

Found?

Search left half

Search right half

End)

TAKEAWAY:
(write summary)

PRACTICE:
(write one question)
"""


@app.route("/")
def home():
    return render_template("index.html")



@app.route("/explain", methods=["POST"])
def explain():

    question = request.form.get("question")
    language = "English"


    prompt = f"""
{SYSTEM_PROMPT}

Language:
{language}

Student Question:
{question}
"""


    try:

        response = client.chat.completions.create(

            model="llama-3.1-8b-instant",

            messages=[
                {
                    "role":"user",
                    "content":prompt
                }
            ],

            max_tokens=500,
            temperature=0.2

        )


        answer = response.choices[0].message.content


        # Remove markdown symbols
        answer = answer.replace("*","")


        concept = extract(answer,"CONCEPT","STEPS")
        steps = extract(answer,"STEPS","EXAMPLE")
        example = extract(answer,"EXAMPLE","FLOWCHART")
        flowchart = extract(answer,"FLOWCHART","TAKEAWAY")
        takeaway = extract(answer,"TAKEAWAY","PRACTICE")        
        practice = extract(answer,"PRACTICE",None)



        return jsonify({

    "concept":concept,
    "steps":steps,
    "example":example,
    "flowchart":flowchart,
    "takeaway":takeaway,
    "practice":practice

})


    except Exception as e:

        return jsonify({

            "concept":"Error generating explanation",
            "steps":str(e),
            "example":"",
            "takeaway":"",
            "practice":""

        })



def extract(text,start,end):

    try:

        if end:

            result = text.split(start)[1].split(end)[0]

        else:

            result = text.split(start)[1]


        result = result.replace(":","",1)
        return result.strip()
        

    except:

        return ""

@app.route("/check_answer", methods=["POST"])
def check_answer():

    practice = request.form.get("practice")
    student_answer = request.form.get("answer")

    prompt = f"""
You are an expert tutor.

Question:
{practice}

Student Answer:
{student_answer}

Evaluate the answer.

Return EXACTLY in this format.

SCORE:
(number out of 10)

FEEDBACK:
(short paragraph)

CORRECT_POINTS:
(Bullet points)

IMPROVEMENT:
(How the student can improve)

ENCOURAGEMENT:
(One motivational sentence)
"""

    try:

        response = client.chat.completions.create(

            model="llama-3.1-8b-instant",

            messages=[
                {
                    "role":"user",
                    "content":prompt
                }
            ],

            temperature=0.2,

            max_tokens=350

        )

        answer = response.choices[0].message.content

        return jsonify({

            "feedback":answer

        })

    except Exception as e:

        return jsonify({

            "feedback":str(e)

        })


if __name__=="__main__":

    app.run(debug=True)