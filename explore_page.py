import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

def shorten_categories(categories, cutoff):
    categorical_map = {}
    for i in range(len(categories)):
        if categories.values[i] >= cutoff:
            categorical_map[categories.index[i]] = categories.index[i]
        else:
            categorical_map[categories.index[i]] = 'Other'
    return categorical_map

def clean_experiance(x):
    if x == 'More than 50 years':
        return 50
    elif x == 'Less than 1 year':
        return 0.5
    return float(x)

def clean_education(x):
    if "Bachelor's degree" in x:
        return "Bachelor's degree"
    if "Master's degree" in x:
        return "Master's Degree"
    if 'Professional degree' in x or 'Other doctoral' in x:
        return 'Post grad'
    return 'less than bachelors'

@st.cache
def load_data():
    data = pd.read_csv('../../../Desktop/stack-overflow-developer-survey-2022/survey_results_public.csv')
    data = data[['Country', 'EdLevel', 'YearsCodePro', 'Employment', 'ConvertedCompYearly']]
    data = data.rename({'ConvertedCompYearly': 'Salary'}, axis=1)
    data = data[data['Salary'].notnull()]
    data = data.dropna()
    data = data[data['Employment']=='Employed, full-time']
    data = data.drop('Employment', axis=1)

    country_map = shorten_categories(data.Country.value_counts(), 400)
    data['Country'] = data['Country'].map(country_map)
    data = data[data['Salary'] <= 250000]
    data = data[data['Salary'] >= 10000]
    data = data[data['Country'] != 'Other']

    data['YearsCodePro'] = data['YearsCodePro'].apply(clean_experiance)
    data['EdLevel'] = data['EdLevel'].apply(clean_education)

    return data

data = load_data()


def show_explore_page():
    st.title("Explore software Engineer Salaries")

    st.write(
        """
        ### Stack Overflow Developer Survey 2022
        """
    )

    df =  data['Country'].value_counts()

    fig1, ax1 = plt.subplots()
    ax1.pie(df, labels=df.index, autopct="%1.1f%%", shadow=True, startangle=90)
    ax1.axis("equal")

    st.write("""#### Data from Different Countries""")

    st.pyplot(fig1)

    st.write("""#### Mean Salary Based On Country""")

    df = data.groupby('Country')['Salary'].mean().sort_values(ascending=True)
    st.bar_chart(df)

    st.write("""#### Mean Salary Based On Experience""")

    df = data.groupby('YearsCodePro')['Salary'].mean().sort_values(ascending=True)
    st.line_chart(df)
