def px_bargrapgh(df):
    
    return px.bar(x=mall_count.index, y=mall_count.values,
                labels={'x': 'Shopping Malls', 'y': 'Count'},
                title='Count of Shopping Malls',
                color=mall_count.index,
                color_discrete_sequence=px.colors.qualitative.Set3).update_layout(xaxis_tickangle=-45)

def gender_payment_viz(df):
    #Knowing which gender use every payment method more
    gender_payment_count = df.groupby(['gender', 'payment_method']).size().reset_index(name='count')

    fig = px.bar(gender_payment_count, x='payment_method', y='count', color='gender',
                barmode='group', title='Payment Method Distribution by Gender',
                color_discrete_sequence=['pink','skyblue'])
    return

def px_pie(df):
    return px.pie(names= payment_method_count.index, values= payment_method_count.values, title= 'Payment Method count')


gender_quantity_count = df.groupby(['gender', 'quantity']).size().reset_index(name= 'count')
def category_count_values(df):
    return px.bar(gender_quantity_count, x='quantity', y='count', color='gender',
             barmode='group', labels={'quantity': 'Quantity', 'count': 'Count'},
             title='Quantity Count for Each Gender',
             color_discrete_sequence=['pink','skyblue'])


gender_category_count = df.groupby(['gender', 'category']).size().reset_index(name= 'count')
def category_count_values(df):
    return px.bar(gender_category_count, x='category', y='count', color='gender',
             barmode='group', labels={'category': 'Category', 'count': 'Count'},
             title='Category Count for Each Gender',
             color_discrete_sequence=['pink','skyblue'])

def plt_figure(df):
    return plt.figure(figsize=(15, 8))
sns.countplot(data=df, x=df['category'], hue=df['gender'], palette=['pink','skyblue'])
plt.title('Category count for each gender')


def category_count_value(df):
    return px.bar(x=category_count.index, y=category_count.values,
             labels={'x': 'Category', 'y': 'Count'},
             title='Count of Each Category',
             color=category_count.index,
             color_discrete_sequence=px.colors.qualitative.Set3).update_layout(xaxis_tickangle=-45)

def barplot_count(df):
    return sns.barplot(x=category_count.index, y=category_count.values)
plt.title('Count of Each Category')
plt.xlabel('Category')
plt.ylabel('Count')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()


def countplot (df):
    return sns.countplot(x='gender', data = df,palette=['pink','skyblue'])
plt.title('Gender distribution')
plt.xlabel('Gender')
plt.ylabel('Count')
plt.show()


def gender_distribution_px(df):
 return px.bar(gender_count,
             title='Gender distribution',
             text_auto=True,
             labels=dict(index='gender', value='count'),
             color_discrete_sequence=[['#FF69B4', '#87CEEB']]).update_xaxes(type='category')

def mean_age(df):
    return px.bar(gender_age, x='gender', y='age', color='gender',
             color_discrete_sequence=['pink', 'skyblue'],
             labels={'gender': 'Gender', 'age': 'Mean Age'},
             title='Mean age by gender').update_xaxes(categoryorder='total ascending')


def barplot_age (df):
    return sns.barplot(x= 'gender', y = 'age', data = gender_age, palette=['pink','skyblue'])
plt.title('Mean age by gender')
plt.xlabel('Gender')
plt.ylabel('Mean Age')
plt.show()