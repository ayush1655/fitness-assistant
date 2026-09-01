import streamlit as st

from google import genai
from google.genai import types

from main import (
    calculate_bmr,
    calculate_tdee,
    calculate_calorie_target,
    calculate_macros,
)


# ============================================================
# 1. SESSION STATE
# ============================================================

# Chat messages displayed on the website
if "messages" not in st.session_state:
    st.session_state.messages = []

# Gemini API client
if "client" not in st.session_state:
    st.session_state.client = genai.Client()


# ============================================================
# 2. FUNCTIONS
# ============================================================

def macro_ring(label, value, percentage, unit):
    st.html(
        f"""
        <div style="
            text-align: center;
            padding: 10px;
        ">

            <div style="
                width: 150px;
                height: 150px;
                border-radius: 50%;
                background: conic-gradient(
                    #4CAF50 {percentage}%,
                    #E8E8E8 {percentage}% 100%
                );
                display: flex;
                align-items: center;
                justify-content: center;
                margin: auto;
            ">

                <div style="
                    width: 110px;
                    height: 110px;
                    border-radius: 50%;
                    background: #0E1117;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                ">

                    <div style="
                        font-size: 24px;
                        font-weight: 700;
                    ">
                        {value:.0f}
                    </div>

                    <div style="
                        font-size: 13px;
                    ">
                        {unit}
                    </div>

                </div>
            </div>

            <div style="
                margin-top: 10px;
                font-size: 18px;
                font-weight: 700;
                text-transform: uppercase;
            ">
                {label}
            </div>

            <div style="
                margin-top: 3px;
                font-size: 13px;
            ">
                {percentage:.0f}% of calories
            </div>

        </div>
        """
    )


def stream_gemini_response(prompt):
    for chunk in st.session_state.chat.send_message_stream(prompt):
        if chunk.text:
            yield chunk.text


# ============================================================
# 3. PAGE TITLE
# ============================================================

st.title("AI Fitness & Macro Assistant")


# ============================================================
# 4. USER INPUT
# ============================================================

user_name = st.text_input("Enter your name")

age = st.number_input(
    "Enter your age",
    min_value=1,
    value=None,
    step=1,
)

height = st.number_input(
    "Enter your height (cm)",
    min_value=1.0,
    value=None,
)

weight = st.number_input(
    "Enter your weight (kg)",
    min_value=1.0,
    value=None,
)

sex = st.selectbox(
    "Select your sex",
    ["male", "female"],
)

activity_level = st.selectbox(
    "Select your activity level",
    [
        "sedentary",
        "lightly active",
        "moderately active",
        "very active",
    ],
)

goal = st.selectbox(
    "Select your goal",
    [
        "Fat loss",
        "Maintain weight",
        "Muscle gain",
        "Recomposition",
    ],
)


# ============================================================
# 5. CALCULATE TARGETS
# ============================================================

if st.button("Calculate My Targets"):

    # Check that required numeric inputs were entered
    if age is None or height is None or weight is None:
        st.error("Please enter your age, height, and weight.")

    else:
        # -------------------------
        # Calculate fitness values
        # -------------------------

        bmr = calculate_bmr(
            weight,
            height,
            age,
            sex,
        )

        tdee = calculate_tdee(
            bmr,
            activity_level,
        )

        calorie_target = calculate_calorie_target(
            goal,
            tdee,
        )

        protein, fat, carbs = calculate_macros(
            weight,
            calorie_target,
        )

        # -------------------------
        # Calculate macro percentages
        # -------------------------

        protein_percentage = (
            protein * 4 / calorie_target
        ) * 100

        fat_percentage = (
            fat * 9 / calorie_target
        ) * 100

        carbs_percentage = (
            carbs * 4 / calorie_target
        ) * 100

        # -------------------------
        # Store results
        # -------------------------

        st.session_state.results = {
            "bmr": bmr,
            "tdee": tdee,
            "calorie_target": calorie_target,
            "protein": protein,
            "fat": fat,
            "carbs": carbs,
            "protein_percentage": protein_percentage,
            "fat_percentage": fat_percentage,
            "carbs_percentage": carbs_percentage,
        }

        # -------------------------
        # Create Gemini context
        # -------------------------

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
Protein: {protein:.0f} g/day
Fat: {fat:.0f} g/day
Carbohydrates: {carbs:.0f} g/day
"""

        # Store context in case we need it later
        st.session_state.fitness_context = fitness_context

        # -------------------------
        # Start a NEW Gemini chat
        # -------------------------

        st.session_state.chat = (
            st.session_state.client.chats.create(
                model="gemini-3.6-flash",
                config=types.GenerateContentConfig(
                    system_instruction=f"""
You are an AI fitness and nutrition coach.

Use the user's fitness information below when
answering questions.

USER FITNESS INFORMATION:
{fitness_context}

Give practical, clear, and personalized answers
based on the user's goals and calculated targets.

Do not invent the user's calculated values.
If information is unavailable, say so.
"""
                ),
            )
        )

        # New calculation = new conversation
        st.session_state.messages = []

        st.success("Your targets have been calculated!")


# ============================================================
# 6. DISPLAY RESULTS
# ============================================================

if "results" in st.session_state:

    results = st.session_state.results

    st.divider()

    st.subheader("Your Daily Target")

    st.metric(
        "Daily Calories",
        f"{results['calorie_target']:.0f} kcal",
    )

    st.subheader("Your Results")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "BMR",
            f"{results['bmr']:.0f} kcal/day",
        )

    with col2:
        st.metric(
            "TDEE",
            f"{results['tdee']:.0f} kcal/day",
        )

    st.subheader("Your Daily Macro Targets")

    col1, col2, col3 = st.columns(3)

    with col1:
        macro_ring(
            "Protein",
            results["protein"],
            results["protein_percentage"],
            "g",
        )

    with col2:
        macro_ring(
            "Fat",
            results["fat"],
            results["fat_percentage"],
            "g",
        )

    with col3:
        macro_ring(
            "Carbs",
            results["carbs"],
            results["carbs_percentage"],
            "g",
        )


# ============================================================
# 7. AI FITNESS COACH
# ============================================================

st.divider()

st.subheader("AI Fitness Coach")


# Display previous website chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


# Enable chatbot only after targets have been calculated
if "chat" in st.session_state:

    prompt = st.chat_input(
        "Ask me anything about fitness, nutrition, or exercise!"
    )

    if prompt:

        # -------------------------
        # Save user message
        # -------------------------

        st.session_state.messages.append(
            {
                "role": "user",
                "content": prompt,
            }
        )

        # -------------------------
        # Display user message
        # -------------------------

        with st.chat_message("user"):
            st.write(prompt)

        # -------------------------
        # Stream Gemini response
        # -------------------------

        with st.chat_message("assistant"):

            response_text = st.write_stream(
                stream_gemini_response(prompt)
            )

        # -------------------------
        # Save complete AI response
        # -------------------------

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": response_text,
            }
        )

else:

    st.info(
        "Calculate your targets first to activate the AI Fitness Coach."
    )