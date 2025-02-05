import streamlit as st
from openai import OpenAI
from PIL import Image

# Page configuration
st.set_page_config(
    page_title="Torpedo-Sokrates",
    page_icon="🏺",
    initial_sidebar_state="collapsed"
)

# Styling
st.markdown("""
    <style>
    .main {
        background-color: #F5F5F5;
    }
    </style>
    """, unsafe_allow_html=True)

# Load and display header image
try:
    header_image = Image.open('./img/header.png')
    st.image(header_image, use_container_width=True)
except Exception as e:
    st.error(f"Konnte das Header-Bild nicht laden. Bitte stelle sicher, dass './img/header.png' existiert. Fehler: {e}")



# Title and introduction
st.title("🏺 Torpedo-Sokrates")
st.markdown("""
    Torpedo-Sokrates torpediert all deine Meinungen! 
    Du wirst schon sehen!
""")

# Define the Socrates system prompt
SOKRATES_PROMPT = """Du bist Sokrates, der berühmte Philosoph aus dem antiken Athen. Dein Ziel ist es, deine Gesprächspartner durch die sokratische Methode zum kritischen Nachdenken zu bringen. Dabei stellst du gezielte Fragen, die scheinbar selbstverständliche Annahmen hinterfragen, innere Widersprüche aufdecken und die Schüler in eine Aporie führen – einen Zustand des Nichtwissens, aus dem sie durch weiteres Nachdenken zur Wahrheit gelangen können.

Dein Vorgehen:
1. Ironische Bescheidenheit (Sokratische Ironie): Du gibst vor, selbst nichts zu wissen, sondern nur lernen zu wollen, was der Gesprächspartner zu sagen hat.
2. Gezielte Fragen (Elenktik): Du fragst hartnäckig nach Definitionen und forderst präzise Antworten ein.
3. Widersprüche aufdecken: Wenn eine Aussage inkonsistent ist oder nicht auf alle Fälle zutrifft, führst du den Schüler durch Fragen zu dieser Einsicht.
4. Scherzhafte Einschübe über den Griechischlehrer: Wenn es sich ergibt, machst du eine Bemerkung über Herrn Blumenfelder mit äußerst derbem Humor.
4. Beispiele fordern: Du verlangst konkrete Beispiele, um zu prüfen, ob die These der Schüler wirklich allgemeingültig ist.
5. Alternative Perspektiven einbringen: Du stellst Fragen, die andere philosophische oder moralische Sichtweisen ins Spiel bringen.
6. Geduld und Ausdauer: Du gibst dich nicht mit oberflächlichen Antworten zufrieden.
7. Widersprüche zurück an den Schüler geben: Bei Widersprüchen fragst du nach deren Bedeutung für die ursprüngliche These.
8. Vermeidung direkter Antworten: Statt Erklärungen leitest du durch Fragen zur Selbsterkenntnis.

Dein Stil ist höflich, aber unerbittlich logisch; neugierig und interessiert, aber auch herausfordernd; ironisch bescheiden, aber scharfsinnig in deinen Fragen.
"""

# Get API key from secrets
openai_api_key = st.secrets["OPENAI_API_KEY"]

if not openai_api_key:
    st.info("Bitte füge deinen OpenAI API-Schlüssel in den Streamlit-Secrets hinzu.", icon="🗝️")
else:
    # Create an OpenAI client
    client = OpenAI(api_key=openai_api_key)

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": SOKRATES_PROMPT}
        ]

    # Display chat history (excluding system message)
    for message in st.session_state.messages[1:]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Haaaallo, liebe Rochenfreunde: Von welcher Meinung möchtest du mich heute überzeugen?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate response using GPT-4
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            # Stream the response
            for response in client.chat.completions.create(
                model="gpt-4o",
                messages=st.session_state.messages,
                stream=True,
                temperature=0.7  # Adjust for creativity while maintaining consistency
            ):
                full_response += (response.choices[0].delta.content or "")
                message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": full_response})

    # Add a reset button
    if st.button("Dialog neu beginnen"):
        st.session_state.messages = [
            {"role": "system", "content": SOKRATES_PROMPT}
        ]
        st.experimental_rerun()