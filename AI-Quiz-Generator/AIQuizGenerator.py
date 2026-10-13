import streamlit as st
from openai import OpenAI
import os
import json

# ----------------------------
# STREAMLIT CONFIG (IMPORTANT)
# ----------------------------
st.set_page_config(
    page_title="AI Quiz Generator",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ----------------------------
# API KEY
# ----------------------------
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    st.error("Missing OPENAI_API_KEY")
    st.stop()

client = OpenAI(api_key=api_key)

# ----------------------------
# QUESTION MODEL
# ----------------------------
class Question:
    def __init__(self, question, options, correct_answer, explanation=None):
        self.question = question
        self.options = options
        self.correct_answer = correct_answer
        self.explanation = explanation

# ----------------------------
# QUIZ ENGINE
# ----------------------------
class Quiz:
    def __init__(self):
        self.init_questions()
        self.init_state()

    def init_questions(self):
        if "questions" not in st.session_state:
            st.session_state.questions = [
                Question(
                    "What is the capital of France?",
                    ["London", "Paris", "Berlin", "Madrid"],
                    "Paris",
                    "Paris is the capital of France."
                ),
                Question(
                    "Who developed relativity?",
                    ["Newton", "Einstein", "Tesla", "Curie"],
                    "Einstein",
                    "Einstein created the theory of relativity."
                )
            ]

        self.questions = st.session_state.questions

    def init_state(self):
        st.session_state.setdefault("index", 0)
        st.session_state.setdefault("score", 0)

    # ----------------------------
    def run(self):
        self.sidebar()

        if st.session_state.index >= len(self.questions):
            self.results()
        else:
            self.question_view()

    # ----------------------------
    def sidebar(self):
        total = len(self.questions)
        index = st.session_state.index
        score = st.session_state.score

        percent = int((score / total) * 100) if total > 0 else 0

        with st.sidebar:
            st.title("🧠 Quiz Dashboard")

            st.markdown("---")

            st.subheader("📊 Score")
            st.write(f"{score} / {total}")

            st.subheader("📈 Success Rate")
            st.write(f"{percent}%")

            st.progress(percent / 100 if total > 0 else 0)

            st.markdown("---")

            st.subheader("📍 Progress")
            st.write(f"{index + 1} / {total}")

            st.progress(index / total if total > 0 else 0)

            st.markdown("---")

            if st.button("🔄 Restart Quiz"):
                self.restart()

    # ----------------------------
    def question_view(self):
        q = self.questions[st.session_state.index]

        st.subheader(q.question)

        answer = st.radio(
            "Choose answer:",
            q.options,
            key=f"q_{st.session_state.index}"
        )

        if st.button("Submit", key=f"btn_{st.session_state.index}"):

            if answer == q.correct_answer:
                st.session_state.score += 1
                st.success("Correct!")
            else:
                st.error("Wrong!")

            if q.explanation:
                st.info(q.explanation)

            st.session_state.index += 1
            st.rerun()

    # ----------------------------
    def results(self):
        st.title("🎉 Quiz Completed")

        st.write(f"Score: {st.session_state.score}/{len(self.questions)}")

        if st.session_state.score == len(self.questions):
            st.success("Perfect score!")
            st.balloons()
        else:
            st.warning("Try again!")

        if st.button("Restart Quiz"):
            self.restart()

    # ----------------------------
    def restart(self):
        st.session_state.index = 0
        st.session_state.score = 0
        st.rerun()

# ----------------------------
# AI GENERATOR
# ----------------------------
def generate_question(topic):
    prompt = """
    Return ONLY valid JSON:
    {
      "question": "",
      "options": ["", "", "", ""],
      "correct": "",
      "explanation": ""
    }
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": f"Topic: {topic}"}
            ]
        )

        data = json.loads(response.choices[0].message.content)

        new_q = Question(
            data["question"],
            data["options"],
            data["correct"],
            data["explanation"]
        )

        st.session_state.questions.append(new_q)

    except Exception as e:
        st.error(f"AI Error: {e}")

# ----------------------------
# APP UI
# ----------------------------
st.title("AI Quiz Generator")

if "quiz" not in st.session_state:
    st.session_state.quiz = Quiz()

topic = st.text_input("Enter topic")

if st.button("Generate Question"):
    if topic:
        generate_question(topic)

st.session_state.quiz.run()