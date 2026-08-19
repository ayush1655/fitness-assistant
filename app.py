import streamlit as st
from google import genai

client = genai.Client()
if "messages" not in st.session_state:
        st.session_state["messages"]=[]


from main import (
                calculate_bmr,
                calculate_tdee,
                calculate_calorie_target,
                calculate_macros
)

st.title("AI Fitness & Macro Assistant")

user_name = st.text_input("Enter your name")

age = st.number_input(
    "Enter your age",
    min_value=1,
    value=None,
    step=1
)

height = st.number_input(
    "Enter your height (cm)",
    min_value=1.0,
    value=None
)

weight = st.number_input(
    "Enter your weight (kg)",
    min_value=1.0,
    value=None
)

sex = st.selectbox(
    "Select your sex",
    ["male", "female"]
)

activity_level = st.selectbox(
               "select your activity level",
               [
                "sedentary",
                "lightly active",
                "moderately active",
                "very active"
                ]
)

goal = st.selectbox(
    "Select your goal",
    [
        "Fat loss",
        "Maintain weight",
        "Muscle gain",
        "Recomposition"
    ]
)

if st.button("Calculate My Targets"):
        bmr = calculate_bmr(weight,height,age,sex)
        tdee = calculate_tdee(bmr,activity_level)
        calorie_target = calculate_calorie_target(goal, tdee)
        protein, fat, carbs = calculate_macros(weight,calorie_target)

        fitness_context = f"""
        User Name: {user_name}
        Age: {age}
        Height: {height} cm
        Weight: {weight} kg
        Sex: {sex}
        Activity Level: {activity_level}
        Goal: {goal}

        BMR: {bmr:.0f} kcal/day
        TDEE: {tdee:.0f} kcal/day
        Calorie Target: {calorie_target:.0f} kcal/day
        Protein: {protein:.0f} g
        Fat: {fat:.0f} g
        Carbs: {carbs:.0f} g
        """

        st.session_state["fitness_context"] = fitness_context

        st.subheader("Your Results")

        col1, col2, col3 = st.columns(3)

        col1.metric("BMR",f"{bmr:.0f} kcal/day")
        col2.metric("TDEE",f"{tdee:.0f} kcal/day")
        col3.metric("Calorie Target",f"{calorie_target:.0f} kcal/day")

        st.subheader("Your Daily Macro Targets")
        col1, col2, col3 = st.columns(3)
        col1.metric("Protein",f"{protein:.0f} g")
        col2.metric("Fat",f"{fat:.0f} g")
        col3.metric("Carbs",f"{carbs:.0f} g")

st.subheader("AI Fitness Coach")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

prompt = st.chat_input("Ask me anything about fitness, nutrition, or exercise!")

if prompt:
        st.session_state.messages.append(
        {"role": "user", "content": prompt}
        )
        # Convert our chat history into Gemini's format
        history = []

        for message in st.session_state.messages:
            gemini_message = {
                "role": message["role"] if message["role"] == "user" else "model",
                "parts": [{"text": message["content"]}]
            }

            history.append(gemini_message)
        history_text = "\n\n".join(
            f'{message["role"].upper()}: {message["content"]}'
            for message in st.session_state.messages
        )

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=f"""
        You are a fitness and nutrition expert.

        Here is the user's fitness context:
        {st.session_state["fitness_context"]}

        Here is the conversation history:
        {history_text}

        User's latest question:
        {prompt}

        Use the conversation history and fitness context to answer the user's latest question.
        """
        )

        with st.chat_message("user"):
                st.write(prompt)

        with st.chat_message("assistant"):
                st.write(response.text)

