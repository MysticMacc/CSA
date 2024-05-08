from flask import Flask, jsonify, render_template
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px


def load_data():
    df = pd.read_csv("static/DATASET/customer_shopping_data.csv")
    df.drop(columns=['invoice_no'], inplace= True)
    df.set_index('customer_id', inplace=True)
    df['invoice_date'] = pd.to_datetime(df['invoice_date'], format='%d/%m/%Y')
    df['year'] = df['invoice_date'].dt.year
    df['month'] = df['invoice_date'].dt.month
    return df

def gender_distribution_px(df):
    gender_count = df['gender'].value_counts()
    return px.bar(gender_count,
    title='Gender distribution',
    text_auto=True,
    labels=dict(index='gender', value='count'),
    color_discrete_sequence=[['#FF69B4', '#87CEEB']]).update_xaxes(type='category')

def category_count_value(df):
    category_count = df['category'].value_counts()
    return px.bar(x=category_count.index, y=category_count.values,
             labels={'x': 'Category', 'y': 'Count'},
             title='Count of Each Category',
             color=category_count.index,
             color_discrete_sequence=px.colors.qualitative.Set3).update_layout(xaxis_tickangle=-45)

def category_count_values(df):
    gender_category_count = df.groupby(['gender', 'category']).size().reset_index(name= 'count')
    return px.bar(gender_category_count, x='category', y='count', color='gender',
             barmode='group', labels={'category': 'Category', 'count': 'Count'},
             title='Category Count for Each Gender',
             color_discrete_sequence=['pink','skyblue'])

def px_pie(df):
    payment_method_count = df['payment_method'].value_counts()
    return px.pie(names= payment_method_count.index, values= payment_method_count.values, title= 'Payment Method count' , hole=.5)


def gender_payment_viz(df):
    #Knowing which gender use every payment method more
    gender_payment_count = df.groupby(['gender', 'payment_method']).size().reset_index(name='count')

    fig = px.bar(gender_payment_count, x='payment_method', y='count', color='gender',
                barmode='group', title='Payment Method Distribution by Gender',
                color_discrete_sequence=['pink','skyblue'])
    return fig

def px_bargrapgh(df):
    mall_count = df['shopping_mall'].value_counts()
    return px.bar(x=mall_count.index, y=mall_count.values,
                labels={'x': 'Shopping Malls', 'y': 'Count'},
                title='Count of Shopping Malls',
                color=mall_count.index,
                color_discrete_sequence=px.colors.qualitative.Set3).update_layout(xaxis_tickangle=-45)



app = Flask(__name__)

#Reading data
data_df = pd.read_csv("static/data/Churn_data.csv")
churn_df = data_df[(data_df['Churn']=="Yes").notnull()] 

@app.route('/')
def index():
    return render_template('index.html')

def calculate_percentage(val, total):
    """Calculates the percentage of a value over a total"""
    percent = np.round((np.divide(val, total) * 100), 2)
    return percent

def data_creation(data, percent, class_labels, group=None):
    for index, item in enumerate(percent):
        data_instance = {}
        data_instance['category'] = class_labels[index]
        data_instance['value'] = item
        data_instance['group'] = group
        data.append(data_instance)

@app.route('/get_piechart_data')
def get_piechart_data():
    contract_labels = ['Month-to-month', 'One year', 'Two year']
    _ = churn_df.groupby('Contract').size().values
    class_percent = calculate_percentage(_, np.sum(_)) #Getting the value counts and total

    piechart_data= []
    data_creation(piechart_data, class_percent, contract_labels)
    return jsonify(piechart_data)

@app.route('/get_barchart_data')
def get_barchart_data():
    tenure_labels = ['0-9', '10-19', '20-29', '30-39', '40-49', '50-59', '60-69', '70-79']
    churn_df['tenure_group'] = pd.cut(churn_df.tenure, range(0, 81, 10), labels=tenure_labels)
    select_df = churn_df[['tenure_group','Contract']]
    contract_month = select_df[select_df['Contract']=='Month-to-month']
    contract_one = select_df[select_df['Contract']=='One year']
    contract_two =  select_df[select_df['Contract']=='Two year']
    _ = contract_month.groupby('tenure_group').size().values
    mon_percent = calculate_percentage(_, np.sum(_))
    _ = contract_one.groupby('tenure_group').size().values
    one_percent = calculate_percentage(_, np.sum(_))
    _ = contract_two.groupby('tenure_group').size().values
    two_percent = calculate_percentage(_, np.sum(_))
    _ = select_df.groupby('tenure_group').size().values
    all_percent = calculate_percentage(_, np.sum(_))

    barchart_data = []
    data_creation(barchart_data,all_percent, tenure_labels, "All")
    data_creation(barchart_data,mon_percent, tenure_labels, "Month-to-month")
    data_creation(barchart_data,one_percent, tenure_labels, "One year")
    data_creation(barchart_data,two_percent, tenure_labels, "Two year")
    return jsonify(barchart_data)

@app.route('/analysis')
def analysis():
    df = load_data()
    fig1 = gender_distribution_px(df)
    fig2 = category_count_value(df)
    fig3 = category_count_value(df)
    fig4 = px_pie(df)
    fig5 =  gender_payment_viz(df)
    fig6 = px_bargrapgh(df)
    return render_template('analysis.html', fig1=fig1.to_html(full_html=False),fig3=fig3.to_html(full_html=False),fig4=fig4.to_html(full_html=False),fig5=fig5.to_html(full_html=False),fig6=fig6.to_html(full_html=False))

    
if __name__ == '__main__':
    app.run(debug=True)
                   