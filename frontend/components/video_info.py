import streamlit as st


def display_video_info(
    video_data: dict
):

    st.subheader(
        "Video Information"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.write(
            "**Title:**",
            video_data.get(
                "title",
                "Unknown"
            )
        )

        st.write(
            "**Video ID:**",
            video_data.get(
                "video_id",
                ""
            )
        )

    with col2:

        st.write(
            "**Chunks:**",
            video_data.get(
                "chunks_created",
                0
            )
        )

        st.success(
            video_data.get(
                "message",
                "Video processed"
            )
        )