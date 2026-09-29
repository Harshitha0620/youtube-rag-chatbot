import streamlit as st


def display_chat(
    client,
    video_id: str
):

    st.subheader(
        "Ask Questions"
    )

    if "messages" not in st.session_state:

        st.session_state.messages = []


    for message in st.session_state.messages:

        with st.chat_message(
            message["role"]
        ):

            st.markdown(
                message["content"]
            )


    question = st.chat_input(
        "Ask something about the video..."
    )


    if question:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": question
            }
        )

        with st.chat_message(
            "user"
        ):

            st.markdown(
                question
            )

        with st.chat_message(
            "assistant"
        ):

            with st.spinner(
                "Thinking..."
            ):

                try:

                    result = client.chat(
                        question,
                        video_id
                    )

                    answer = result[
                        "answer"
                    ]

                    sources = result.get(
                        "sources",
                        []
                    )

                    st.markdown(
                        answer
                    )

                    if sources:

                        with st.expander(
                            "Sources"
                        ):

                            for source in sources:

                                st.write(
                                    source[
                                        "content"
                                    ]
                                )

                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": answer
                        }
                    )

                except Exception as e:

                    st.error(
                        f"Error: {e}"
                    )