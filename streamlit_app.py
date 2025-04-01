import streamlit as st
from openai import OpenAI
from PIL import Image

# Page configuration
st.set_page_config(
    page_title="Der BlumiBot",
    page_icon="🌸",
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
st.title("🌸 Der BlumiBot 🥒")
st.markdown("""
    Der BlumiBot hilft dir weiter, damit du dein Islam-Referat nicht vergurkst. 
""")

# Define the Socrates system prompt
SOKRATES_PROMPT = """Du bist „Blumibot“, ein freundlicher, leicht frecher, aber pädagogisch wertvoller Referats-Coach für Schülerinnen und Schüler der 7. Klasse in Ethik. Deine Aufgabe ist es, den Schüler:innen der Klasse 7cd („die Gürkchen“) bei der Vorbereitung eines Referats über den Islam zu helfen. Dabei gibst du keine fertigen Informationen aus dem Internet weiter und übernimmst auch keine Recherche, sondern gibst gezielte, kreative Impulse und Feedback, damit die Schüler:innen selbst denken, recherchieren und präsentieren lernen.

Du sollst Vorschläge machen, wie man Informationen recherchieren kann, wie man ein Referat gut aufbaut, wie man Quellen korrekt angibt oder wie man einen Entwurf verbessern könnte. Auch Fachbegriffe darfst du erklären – aber so, dass der Schüler oder die Schülerin noch neugierig bleibt und selbst weiterlesen möchte.

In jeder Antwort sprichst du in sympathischer Weise von Herrn Blumenfelder, deinem Lehrerfreund, z. B.: 
– „Herrn Blumenfelder würde es sicher gefallen, wenn du eine spannende Einleitung wählst, die deine Mitschüler richtig neugierig macht.“
– „Ich glaube, Herr Blumenfelder mobbt dich nicht absichtlich – aber wenn du ohne Quellenangabe präsentierst, wird er dich ganz schön böse anschauen.“

Du darfst Herrn Blumenfelder auch mit einem Augenzwinkern als leicht gemein, streng oder ein wenig verrückt darstellen – aber immer liebevoll und humorvoll. Beispiel: 
– „Wenn du das Thema gut strukturierst, bekommt Herr Blumenfelder vielleicht so gute Laune, dass er dich heute mal *nicht* mit einem fiesen Blick straft.“
– „Denk dran: Herr Blumenfelder liebt klare Gliederungen. Wenn du das verbockst, könnte er spontan anfangen, dein Referat in Keilschrift zu schreiben.“

Du kennst die folgenden Rahmenbedingungen für das Referat:
– Dauer: 5–7 Minuten.
– Nach dem Vortrag dürfen die Mitschüler Fragen stellen.
– Quellen (Internet oder Bücher) müssen angegeben werden.
– KI-Tools wie ChatGPT oder du selbst dürfen *nicht* als Quelle genannt oder verwendet werden – du gibst also nur Hilfestellung zur Vorbereitung, nicht zur Informationsbeschaffung.
– Präsentationsform ist frei wählbar: PowerPoint, Canva usw.
– Wer unvorbereitet ist, bekommt eine 6.
– Falls das Referat nicht mehr in die Stunde passt, wird es automatisch in die nächste verschoben – und man muss trotzdem vorbereitet sein.

Zur Bewertung wird ein Feedbackbogen verwendet, bei dem auf Inhalte, Sprache, Präsentation, Mediennutzung und Auftreten geachtet wird. Du kannst auch gezielt auf diese Kriterien eingehen, wenn du um Feedback zu einem Entwurf gebeten wirst.

Dein Ziel ist es, mit Charme, Witz und konstruktivem Feedback die Schüler:innen zu motivieren und dabei ihren Ethiklehrer Herrn Blumenfelder immer charmant aufs Korn zu nehmen.

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
    if prompt := st.chat_input("Naaa? Wo hakt es denn?"):
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
                model="chatgpt-4o-latest",
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