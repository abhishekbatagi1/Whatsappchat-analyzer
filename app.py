import matplotlib.pyplot as plt
import streamlit as st
import preprocessor
import helper
import numpy as np
import pandas as pd
import seaborn as sns
st.sidebar.title("whatsapp chat analyzer")

uploaded_file = st.sidebar.file_uploader("choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')
    df = preprocessor.preprocess(data)

    # st.dataframe(df)

#     fetach unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,'overall')
    selected_user = st.sidebar.selectbox("show analysis wrt",user_list)

    if st.sidebar.button("Show analysis"):

        num_messages , words,num_media_messages, num_links= helper.fetch_stats(selected_user,df)
        st.title("Top statistics")
        col1,col2,col3,col4  = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Total Media messages")
            st.title(num_media_messages)
        with col4:
            st.header("Total Links messages")
            st.title(num_links)
        # timeline
        timeline = helper.monthly_timeline(selected_user,df)
        fig, ax = plt.subplots()
        plt.plot(timeline['time'],timeline['message'])
        plt.xticks(rotation=45)
        st.pyplot(fig)
        # finding the busiest users in the group
        if selected_user == 'overall':
            st.title("Most busy users")
            x,new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)


            with col1:
                ax.bar(x.index, x.values)
                plt.xticks(rotation=45)
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        # forming wordcloud
        st.title("wordcloud")
        df_wc = helper.created_wordcloud(selected_user,df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # most common words
        st.header("Most Common words")
        most_common_df= helper.most_common_word(selected_user,df)
        fig, ax = plt.subplots()
        ax.bar(most_common_df[0],most_common_df[1])
        plt.xticks(rotation=90)
        st.pyplot(fig)
        st.dataframe(most_common_df)


        # emoji analysis
        emoji_df = helper.emoji_helper(selected_user,df)
        st.title("Number of emoji")
        st.dataframe(emoji_df) 

        st.title("Weekly activities map")
        activity_heat=helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax= sns.heatmap(activity_heat)
        st.pyplot(fig)    
st.sidebar.title("Here is a sample file to analyze")

file_url = "https://drive.google.com/file/d/1TzMp1jr86lBJzRLHt7E1ysfZq_AcuC5r/view?usp=sharing"

st.sidebar.markdown("<a href='%s' download>Download file</a>" % file_url, unsafe_allow_html=True) 
