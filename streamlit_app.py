import streamlit as st
import cv2
from PIL import Image
import numpy as np

TITLE = "Traya Performance Academy"

model_reinforcement = { 
    "neutral": 0,
    "helpful": 1,
    "harmful": -1
}

mode = st.query_params.get("mode", "athlete")
action = st.query_params.get("action", "upload")
athlete = st.query_params.get("athlete", "1")
workout = st.query_params.get("workout", "1")
feedback = st.query_params.get("feedback", "0")
superman_mode = st.query_params.get("superman", "0")
last_model_reinforcement = st.query_params.get("model_feedback", "neutral")

last_model_reinforcement_score = model_reinforcement[last_model_reinforcement]

if 'messages' not in st.session_state:
    st.session_state.messages = []


if mode not in ('athlete', 'coach'):
    st.markdown("### ❗Invalid Mode, try again.")
    st.markdown("Login is a [Coach](?mode=coach) or an [Athlete](?mode=athlete)")

feedback_id = int(feedback)
athlete_id = int(athlete)
workout_id = int(workout)
is_superman = int(superman_mode)

def feedback_ready(image):
    # first, we store the image in our repository
    return False


def helpful_feedback():
    if mode == "coach":
        coach_feedback[workout_id][feedback_id]['helpful'] += 1
    else:
        athlete_feedback[workout_id][feedback_id]['helpful'] += 1

def harmful_feedback():
    if mode == "coach":
        coach_feedback[workout_id][feedback_id]['harmful'] += 1
    else:
        athlete_feedback[workout_id][feedback_id]['harmful'] += 1



def save_result():
    # TODO: we need a callback to our persistence server here
    pass


# def run_traya_engine(image):
#     points = get_pose_points_from_image(image)
#     issue, ns, nb, angle = analyze_stride(points)
#     ideal_points = generate_ideal(points)
#     overlay_image = draw_overlay_on_image(image, points, ideal_points)
#     return overlay_image


athlete_feedback = {
    1: {
        0: {
            'helpful': 0,
            'harmful': 0
        },
        1: {
            'helpful': 0,
            'harmful': 0
        },

    }
}

coach_feedback = {
    1: {
        0: {
            'helpful': 0,
            'harmful': 0
        },
        1: {
            'helpful': 0,
            'harmful': 0
        },

    }
}

feedback = {
    1: [
        {
            'observation': 'Your foot is landing in front of your body instead of under you',
            'reason': "Increases ground contact time and reduces stride efficiency.",
            'what_to_look_for': [
                'Foot landing in front of hip',
                'Forward shin angle',
                'Long backside'
            ]
        },
        {
            'observation': 'Your foot is landing in front of your body instead of under you.'
        }
    ]
}

option = None

if is_superman:
    option = st.radio(
            "⚙️ Configuration Panel",
            ["Coach Mode", "Athlete Mode"],
            horizontal=True
        )

if option:
    if option == "Coach Mode":
        mode = "coach"
    else:
        mode = "athlete"

if action == 'ben':
    if prompt := st.chat_input("How can I help?"):
        with st.chat_message("user"):
            st.markdown(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})
            system_response = '''Good, better, best. Never let it rest, till your good gets better, and your better gets best. 
            <img src="https://media1.tenor.com/m/bDeid5bnzmIAAAAd/good-better-best-ben-johnson.gif"/>'''
            st.markdown(system_response, unsafe_allow_html=True)
            st.session_state.messages.append({"role": "system", "content": system_response})

if action == "upload":
    st.set_page_config(layout="wide")
    st.title(TITLE)

    if mode == "coach":
        st.subheader("Analyze your athletes peformance (upload or video)")
    else:   
        st.subheader("Analyze my performance (upload or video)")

    uploaded_file = st.file_uploader("Upload image or video", type=["jpg", "png", "mp4"])

    if uploaded_file is not None:
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        image = cv2.imdecode(file_bytes, 1)
        st.image(image, caption="Uploaded Frame", width='stretch')
        if st.button("Analyze"):
            if feedback_ready(image):
                if st.button("Get Feedback"):
                    st.rerun()
            else:
                st.markdown("### Thank you! Your analytics are being processed by our team of highly educated gerbils....")
                st.markdown("#### In the meantime, feel free to ask your questions to [Ben](?action=ben), our virtual coach")
                if is_superman:
                    st.markdown(f'''<h5> ⚙️ Click <a href="?mode={mode}&action=feedback" target="_self">here</a> to simulate a complete analysis</h5>''',
                        unsafe_allow_html=True)

elif action == "feedback":

    st.set_page_config(layout="wide")
    st.title(TITLE)

    if mode == "coach":
        st.markdown("## Coach Dashboard : Feedback ")
        st.markdown("### 📊 Why It Matters")
        st.write(feedback[workout_id][feedback_id]['reason'])

        st.markdown("### 👁 What to Look For")
        for lookfor in feedback[workout_id][feedback_id]['what_to_look_for']:
            st.write(f'- {lookfor}')
        st.write("|||| Image Overlay will go here ||||")
    else:
        st.markdown("## Athlete Dashboard : Feedback ")
        st.markdown("### 👁")
        st.write("Your foot is landing in front of your body instead of under you.")
        st.write("|||| Image Overlay will go here ||||")
    if st.button("Fix it"):
        st.markdown("### 🎯 Constraint")
        st.write("Use slightly tighter wicket spacing")
        if mode == "coach":
            st.markdown("### 🗣 Coach Check")
            st.write("Does it look like he’s striking under now?")
            st.write(f'''<h3><a href="?mode={mode}&model_feedback=helpful&action=celebrate" target="_self">Yes</a> | <a href="?mode={mode}&model_feedback=harmful&action=celebrate" target="_self">No</a></h5>''', unsafe_allow_html=True)
        else:
            st.markdown("### 🗣 Feel")
            st.write("Did it feel faster under you?")
            st.write(f'''<h3><a href="?mode={mode}&model_feedback=helpful&action=celebrate" target="_self">Yes</a> | <a href="?mode={mode}&model_feedback=harmful&action=celebrate" target="_self">No</a></h5>''', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Analyze Another"):
                st.query_params.clear()
                st.rerun()
        with col2:
            if st.button("Save Result"):
                st.query_params.clear()
                st.rerun()
if action == "celebrate":
    if last_model_reinforcement_score > 0:
        helpful_feedback()
        st.markdown("### ✅ Awesome! Keep going! You are almost there...")
    if last_model_reinforcement_score < 0:
        harmful_feedback()
        st.markdown("### 📋 Noted, Lets try something else...")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Analyze Another"):
            st.query_params.clear()
            st.rerun()
    with col2:
        if st.button("Save Result"):
            st.query_params.clear()
            st.rerun()


