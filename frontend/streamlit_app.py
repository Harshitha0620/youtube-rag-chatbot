import streamlit as st
import requests

from api_client import (
    ingest_video,
    chat,
    summary
)


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(

    page_title="YouTube AI Assistant",

    page_icon="▶️",

    layout="wide"
)


# =========================================================
# SESSION STATE
# =========================================================

if "video_id" not in st.session_state:

    st.session_state.video_id = None


if "video_title" not in st.session_state:

    st.session_state.video_title = None


if "video_url" not in st.session_state:

    st.session_state.video_url = None


if "video_processed" not in st.session_state:

    st.session_state.video_processed = False


if "chat_history" not in st.session_state:

    st.session_state.chat_history = []


if "video_summary" not in st.session_state:

    st.session_state.video_summary = None


# =========================================================
# HEADER
# =========================================================

st.title("▶️ YouTube RAG Chatbot")

st.caption(
    "AI-powered YouTube video analysis using "
    "RAG, Ollama Llama 3.2 and BGE-M3"
)

st.divider()


# =========================================================
# YOUTUBE URL
# =========================================================

st.subheader("YouTube Video")

youtube_url = st.text_input(

    "YouTube URL",

    placeholder="Paste your YouTube video URL here"
)


process_button = st.button(

    "Process Video",

    type="primary",

    use_container_width=True
)


# =========================================================
# PROCESS VIDEO
# =========================================================

if process_button:

    if not youtube_url.strip():

        st.warning(
            "Please enter a YouTube video URL."
        )

    else:

        with st.spinner(
            "Processing YouTube transcript..."
        ):

            try:

                result = ingest_video(
                    youtube_url.strip()
                )


                # Save video information

                st.session_state.video_id = result.get(
                    "video_id"
                )


                st.session_state.video_title = result.get(
                    "title",
                    "YouTube Video"
                )


                st.session_state.video_url = (
                    youtube_url.strip()
                )


                st.session_state.video_processed = True


                # Reset previous conversation

                st.session_state.chat_history = []


                # Reset previous summary

                st.session_state.video_summary = None


                st.success(
                    "Video processed successfully!"
                )


            except requests.exceptions.ConnectionError:

                st.error(
                    "Cannot connect to FastAPI. "
                    "Please make sure FastAPI is running."
                )


            except requests.exceptions.HTTPError as e:

                st.error(
                    f"FastAPI returned an error: {e}"
                )


            except Exception as e:

                st.error(
                    f"Video processing failed: {e}"
                )


# =========================================================
# CURRENT VIDEO
# =========================================================

if st.session_state.video_processed:

    st.divider()

    st.subheader("Current Video")


    st.write(
        f"**Title:** "
        f"{st.session_state.video_title}"
    )


    st.write(
        f"**Video ID:** "
        f"`{st.session_state.video_id}`"
    )


    if st.session_state.video_url:

        st.link_button(

            "▶️ Open YouTube Video",

            st.session_state.video_url
        )


    # =====================================================
    # BUTTONS
    # =====================================================

    col1, col2 = st.columns(2)


    with col1:

        summary_button = st.button(

            "📝 Generate Summary",

            use_container_width=True
        )


    with col2:

        clear_button = st.button(

            "🗑️ Clear Conversation",

            use_container_width=True
        )


    # =====================================================
    # CLEAR CHAT
    # =====================================================

    if clear_button:

        st.session_state.chat_history = []

        st.rerun()


    # =====================================================
    # SUMMARY
    # =====================================================

    if summary_button:

        with st.spinner(
            "Generating summary..."
        ):

            try:

                result = summary(

                    st.session_state.video_id
                )


                if isinstance(
                    result,
                    dict
                ):

                    summary_text = result.get(

                        "summary",

                        "No summary was generated."
                    )

                else:

                    summary_text = str(result)


                st.session_state.video_summary = (
                    summary_text
                )


            except Exception as e:

                st.error(
                    f"Summary generation failed: {e}"
                )


    # =====================================================
    # DISPLAY SUMMARY
    # =====================================================

    if st.session_state.video_summary:

        st.divider()

        st.subheader("📝 Video Summary")

        st.write(
            st.session_state.video_summary
        )


    # =====================================================
    # CHAT
    # =====================================================

    st.divider()

    st.subheader(
        "Ask Questions About the Video"
    )


    # =====================================================
    # CHAT HISTORY
    # =====================================================

    for message in st.session_state.chat_history:


        # User message

        with st.chat_message("user"):

            st.write(
                message["question"]
            )


        # Assistant message

        with st.chat_message("assistant"):

            st.write(
                message["answer"]
            )


            sources = message.get(
                "sources",
                []
            )


            if sources:

                with st.expander(
                    "📚 View Retrieved Sources"
                ):

                    for index, source in enumerate(

                        sources,

                        start=1
                    ):

                        st.markdown(
                            f"**Source {index}**"
                        )


                        if isinstance(
                            source,
                            dict
                        ):

                            st.write(
                                source.get(
                                    "content",
                                    ""
                                )
                            )

                        else:

                            st.write(
                                source
                            )


                        st.divider()


    # =====================================================
    # CHAT INPUT
    # =====================================================

    question = st.chat_input(

        "Ask something about this video..."
    )


    # =====================================================
    # ASK QUESTION
    # =====================================================

    if question:

        # User question

        with st.chat_message("user"):

            st.write(question)


        # AI response

        with st.chat_message("assistant"):

            with st.spinner(
                "Searching the video and generating an answer..."
            ):

                try:

                    result = chat(

                        st.session_state.video_id,

                        question
                    )


                    answer = result.get(

                        "answer",

                        "No answer was generated."
                    )


                    sources = result.get(

                        "sources",

                        []
                    )


                    # Display answer

                    st.write(answer)


                    # Display sources

                    if sources:

                        with st.expander(
                            "📚 View Retrieved Sources"
                        ):

                            for index, source in enumerate(

                                sources,

                                start=1
                            ):

                                st.markdown(
                                    f"**Source {index}**"
                                )


                                if isinstance(
                                    source,
                                    dict
                                ):

                                    st.write(
                                        source.get(
                                            "content",
                                            ""
                                        )
                                    )

                                else:

                                    st.write(
                                        source
                                    )


                                st.divider()


                    # Save chat

                    st.session_state.chat_history.append(

                        {
                            "question": question,

                            "answer": answer,

                            "sources": sources
                        }
                    )


                except requests.exceptions.ConnectionError:

                    st.error(
                        "Cannot connect to FastAPI."
                    )


                except requests.exceptions.HTTPError as e:

                    st.error(
                        f"FastAPI error: {e}"
                    )


                except Exception as e:

                    st.error(
                        f"Unable to generate answer: {e}"
                    )


# =========================================================
# GET STARTED
# =========================================================

else:

    st.divider()

    st.subheader("Get Started")

    st.write(
        "1. Enter a YouTube video URL."
    )

    st.write(
        "2. Click **Process Video**."
    )

    st.write(
        "3. Wait for the transcript to be processed."
    )

    st.write(
        "4. Generate a summary or ask questions."
    )

    st.write(
        "5. The system retrieves relevant transcript "
        "chunks from ChromaDB before generating an answer."
    )