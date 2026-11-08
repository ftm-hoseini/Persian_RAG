
import streamlit as st

from src.main import generate_answer


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="دستیار هوشمند فارسی",
    page_icon="✦",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ==================================================
# CUSTOM CSS
# ==================================================

st.markdown(
    """
    <style>

    @import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;600;700;800&display=swap');


    /* COLOR PALETTE */

    :root {
        --background: #FAF7F6;
        --surface: #FFFFFF;
        --surface-soft: #F5ECEF;

        --primary: #70263D;
        --primary-light: #A34D68;

        --secondary: #B99A68;

        --text: #35252B;
        --muted: #89767D;

        --border: #EADDE1;
    }


    /* GENERAL */

    html,
    body,
    [class*="css"] {
        font-family: 'Vazirmatn', Tahoma, sans-serif !important;
        direction: rtl;
    }

    .stApp {
        background: var(--background) !important;
        color: var(--text) !important;
    }

    [data-testid="stAppViewContainer"] {
        background: var(--background) !important;
    }

    [data-testid="stHeader"] {
        background: transparent !important;
    }

    #MainMenu,
    footer {
        visibility: hidden;
    }

    .block-container {
        max-width: 820px;
        padding-top: 2.5rem;
        padding-bottom: 5rem;
    }


    /* HEADER */

    .hero {
        text-align: center;
        padding: 35px 15px 40px;
    }

    .logo {
        display: inline-flex;
        align-items: center;
        justify-content: center;

        width: 54px;
        height: 54px;

        border-radius: 17px;

        background: var(--primary);
        color: #FFFFFF;

        font-size: 23px;
        font-weight: 700;

        margin-bottom: 18px;

        box-shadow: 0 6px 20px #70263D22;
    }

    .hero h1 {
        color: var(--primary);
        font-size: 2rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -1px;
    }


    /* CHAT MESSAGES */

    [data-testid="stChatMessage"] {
        background: var(--surface) !important;

        border: 1px solid var(--border) !important;
        border-radius: 18px !important;

        padding: 18px !important;
        margin-bottom: 14px;

        direction: rtl;

        box-shadow: 0 3px 12px #70263D08;
    }

    [data-testid="stChatMessage"] p,
    [data-testid="stChatMessage"] li {
        direction: rtl;
        text-align: right;

        color: var(--text) !important;

        font-family: 'Vazirmatn', Tahoma, sans-serif !important;

        font-size: 0.95rem;
        line-height: 2.1;
    }

    [data-testid="stChatMessage"] code {
        direction: ltr;
        font-family: Consolas, monospace;
    }


    /* BOTTOM AREA */

    [data-testid="stBottom"] {
        background: var(--background) !important;
        border-top: none !important;
    }

    [data-testid="stBottom"] > div {
        background: var(--background) !important;
    }

    [data-testid="stBottomBlockContainer"] {
        background: var(--background) !important;

        padding-top: 15px !important;
        padding-bottom: 20px !important;
    }


    /* CHAT INPUT */

    [data-testid="stChatInput"] {
        background: #FFFFFF !important;
        background-color: #FFFFFF !important;

        border: 1.5px solid #DCC5CD !important;
        border-radius: 17px !important;

        box-shadow: 0 4px 18px #70263D10 !important;

        transition: border-color 0.2s ease,
                    box-shadow 0.2s ease;
    }

    [data-testid="stChatInput"]:focus-within {
        border-color: var(--primary-light) !important;

        box-shadow: 0 4px 20px #70263D18 !important;
    }


    /* TYPED TEXT */

    [data-testid="stChatInput"] textarea,
    [data-testid="stChatInput"] textarea:focus {
        background: transparent !important;

        color: #FAF7F6 !important;
        -webkit-text-fill-color: #FAF7F6 !important;

        font-family: 'Vazirmatn', Tahoma, sans-serif !important;
        font-size: 0.95rem !important;

        direction: rtl !important;
        text-align: right !important;

        caret-color: #FAF7F6 !important;
    }


    /* PLACEHOLDER */

    [data-testid="stChatInput"] textarea::placeholder {
        color: #B99A9F !important;
        -webkit-text-fill-color: #B99A9F !important;

        opacity: 1 !important;
    }


    /* SEND BUTTON */

    [data-testid="stChatInput"] button {
        background: var(--primary) !important;
        color: #FFFFFF !important;

        border-radius: 11px !important;
        border: none !important;
    }

    [data-testid="stChatInput"] button:hover {
        background: var(--primary-light) !important;
    }


    /* SOURCES EXPANDER */

    [data-testid="stExpander"] {
        background: var(--surface-soft) !important;

        border: 1px solid var(--border) !important;
        border-radius: 13px !important;
    }

    [data-testid="stExpander"] summary {
        color: var(--primary) !important;

        font-family: 'Vazirmatn', Tahoma, sans-serif !important;
        font-weight: 600;
    }

    [data-testid="stExpander"] p {
        font-family: 'Vazirmatn', Tahoma, sans-serif !important;

        color: var(--text) !important;

        direction: rtl;
        text-align: right;
    }


    /* SPINNER */

    [data-testid="stSpinner"] p {
        font-family: 'Vazirmatn', Tahoma, sans-serif !important;

        color: var(--primary) !important;

        direction: rtl;
    }


    /* ERROR MESSAGES */

    [data-testid="stAlert"] {
        border-radius: 13px;

        font-family: 'Vazirmatn', Tahoma, sans-serif !important;

        direction: rtl;
    }

    </style>
    """,
    unsafe_allow_html=True,
)



# ==================================================
# HEADER
# ==================================================

st.markdown(
    """
    <div class="hero">
        <div class="logo">✦</div>
        <h1>دستیار هوشمند فارسی</h1>
    </div>
    """,
    unsafe_allow_html=True,
)


# ==================================================
# SESSION STATE
# ==================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


# ==================================================
# CHAT HISTORY
# ==================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.write(message["content"])

        if message["role"] == "assistant" and message.get("sources"):

            with st.expander("📚 منابع استفاده‌شده"):

                for source in message["sources"]:
                    st.write(f"• {source}")


# ==================================================
# USER INPUT
# ==================================================

question = st.chat_input(
    "سؤالت را درباره اسناد وارد کن..."
)


if question:

    # Save user question

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    with st.chat_message("user"):
        st.write(question)


    # Generate answer

    with st.chat_message("assistant"):

        with st.spinner("در حال جست‌وجو در اسناد و تولید پاسخ..."):

            try:

                result = generate_answer(question)

                # Handle different return formats

                if isinstance(result, dict):

                    answer = result.get(
                        "answer",
                        "پاسخی دریافت نشد."
                    )

                    sources = result.get("sources", [])

                elif isinstance(result, tuple):

                    answer = result[0]

                    sources = (
                        result[1]
                        if len(result) > 1
                        else []
                    )

                else:

                    answer = result
                    sources = []


                # Display answer

                st.write(answer)


                # Display sources

                if sources:

                    with st.expander("📚 منابع استفاده‌شده"):

                        for source in sources:
                            st.write(f"• {source}")


                # Save assistant response

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer,
                        "sources": sources,
                    }
                )


            except Exception as error:

                st.error(
                    f"خطا در پردازش سؤال: {error}"
                )

