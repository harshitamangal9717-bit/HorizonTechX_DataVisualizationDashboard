import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# page setting
st.set_page_config(
    page_title="Student Performance Dashboard",
    page_icon="📊",
    layout="wide"
)

# simple css for better look
st.markdown("""
<style>
.main-title {
    background: linear-gradient(90deg, #1f4e79, #4776e6);
    padding: 25px;
    border-radius: 15px;
    text-align: center;
    margin-bottom: 20px;
}

.main-title h1 {
    color: white;
    font-size: 38px;
    margin-bottom: 5px;
}

.main-title p {
    color: #e8f0ff;
    font-size: 17px;
}

.card {
    background-color: white;
    padding: 18px;
    border-radius: 12px;
    box-shadow: 0px 2px 10px rgba(0,0,0,0.10);
    text-align: center;
    border-left: 5px solid #1f4e79;
}

.card h3 {
    font-size: 17px;
    color: #1f4e79;
}

.card h2 {
    font-size: 30px;
    color: #222222;
}

.section {
    background-color: #f0f4ff;
    padding: 12px;
    border-radius: 10px;
    margin-top: 18px;
    margin-bottom: 12px;
    border-left: 5px solid #4776e6;
}

.section h3 {
    color: #222222;
}
</style>
""", unsafe_allow_html=True)

# dataset load
df = pd.read_csv("dataset/cleaned_student_performance.csv")

# title
st.markdown("""
<div class="main-title">
    <h1>📊 Student Performance Dashboard</h1>
    <p>Data Visualization Dashboard using Python and Streamlit</p>
</div>
""", unsafe_allow_html=True)

# sidebar filters
st.sidebar.header("Filter Data")

gender = st.sidebar.multiselect(
    "Gender",
    df["gender"].unique(),
    default=df["gender"].unique()
)

result = st.sidebar.multiselect(
    "Result",
    df["result"].unique(),
    default=df["result"].unique()
)

grade = st.sidebar.multiselect(
    "Grade",
    df["grade"].unique(),
    default=df["grade"].unique()
)

# filtering data
filtered_df = df[
    (df["gender"].isin(gender)) &
    (df["result"].isin(result)) &
    (df["grade"].isin(grade))
]

# if no data found
if filtered_df.empty:
    st.warning("No data found for selected filters.")
    st.stop()

# KPI values
total_students = len(filtered_df)
pass_students = len(filtered_df[filtered_df["result"] == "Pass"])
fail_students = len(filtered_df[filtered_df["result"] == "Fail"])
average_score = filtered_df["average_score"].mean()

# summary section
st.markdown('<div class="section"><h3>📌 Overall Summary</h3></div>', unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class="card">
        <h3>Total Students</h3>
        <h2>{total_students}</h2>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="card">
        <h3>Pass Students</h3>
        <h2>{pass_students}</h2>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="card">
        <h3>Fail Students</h3>
        <h2>{fail_students}</h2>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="card">
        <h3>Average Score</h3>
        <h2>{average_score:.2f}</h2>
    </div>
    """, unsafe_allow_html=True)

# charts section
st.markdown('<div class="section"><h3>📈 Charts and Visual Analysis</h3></div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Pass vs Fail Count")
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.countplot(x="result", data=filtered_df, ax=ax)
    ax.set_xlabel("Result")
    ax.set_ylabel("Number of Students")
    st.pyplot(fig)

with col2:
    st.subheader("Grade Distribution")
    fig, ax = plt.subplots(figsize=(6, 4))
    grade_order = ["A+", "A", "B", "C", "D", "F"]
    sns.countplot(x="grade", data=filtered_df, order=grade_order, ax=ax)
    ax.set_xlabel("Grade")
    ax.set_ylabel("Number of Students")
    st.pyplot(fig)

col3, col4 = st.columns(2)

with col3:
    st.subheader("Average Score Distribution")
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.histplot(filtered_df["average_score"], bins=15, kde=True, ax=ax)
    ax.set_xlabel("Average Score")
    ax.set_ylabel("Students Count")
    st.pyplot(fig)

with col4:
    st.subheader("Test Preparation vs Average Score")
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(
        x="test preparation course",
        y="average_score",
        data=filtered_df,
        ax=ax
    )
    ax.set_xlabel("Test Preparation")
    ax.set_ylabel("Average Score")
    st.pyplot(fig)

col5, col6 = st.columns(2)

with col5:
    st.subheader("Subject-wise Average Score")

    subject_avg = {
        "Math": filtered_df["math score"].mean(),
        "Reading": filtered_df["reading score"].mean(),
        "Writing": filtered_df["writing score"].mean()
    }

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(subject_avg.keys(), subject_avg.values())
    ax.set_xlabel("Subject")
    ax.set_ylabel("Average Score")
    st.pyplot(fig)

with col6:
    st.subheader("Math Score vs Reading Score")
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.scatterplot(
        x="math score",
        y="reading score",
        hue="result",
        data=filtered_df,
        ax=ax
    )
    ax.set_xlabel("Math Score")
    ax.set_ylabel("Reading Score")
    st.pyplot(fig)

# heatmap section
st.markdown('<div class="section"><h3>🔥 Correlation Heatmap</h3></div>', unsafe_allow_html=True)

numeric_data = filtered_df.select_dtypes(include=["int64", "float64"])

fig, ax = plt.subplots(figsize=(9, 5))
sns.heatmap(numeric_data.corr(), annot=True, ax=ax)
ax.set_title("Correlation Between Numeric Columns")
st.pyplot(fig)

# top students
st.markdown('<div class="section"><h3>🏆 Top 5 Students</h3></div>', unsafe_allow_html=True)

top_students = filtered_df.sort_values(by="average_score", ascending=False).head(5)
st.dataframe(top_students, use_container_width=True)

# complete data
st.markdown('<div class="section"><h3>📄 Filtered Dataset</h3></div>', unsafe_allow_html=True)
st.dataframe(filtered_df, use_container_width=True)

# download option
csv_data = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Filtered Data",
    data=csv_data,
    file_name="filtered_student_data.csv",
    mime="text/csv"
)

# insights
st.markdown('<div class="section"><h3>💡 Insights</h3></div>', unsafe_allow_html=True)

st.write("""
- This dashboard shows overall student performance in a simple visual format.
- Filters help to analyze data based on gender, result and grade.
- Pass and fail count gives a quick idea of overall result.
- Grade distribution shows the academic level of students.
- Subject-wise chart compares Math, Reading and Writing scores.
- Correlation heatmap helps to understand relation between score columns.
""")