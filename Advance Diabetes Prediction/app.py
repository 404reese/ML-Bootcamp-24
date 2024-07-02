# python -m streamlit run app.py

# libraries
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas



# Load data
df = pd.read_csv('diabetes.csv')

# Streamlit app layout
st.title('Diabetes Checkup')
st.sidebar.header('Patient Data')
st.subheader('Training Data Stats')
st.write(df.describe())

# Split data
x = df.drop(['Outcome'], axis=1)
y = df['Outcome']
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)

# Sidebar function to get user data
def user_report():
    pregnancies = st.sidebar.slider('Pregnancies', 0, 17, 3)
    glucose = st.sidebar.slider('Glucose', 0, 200, 120)
    bp = st.sidebar.slider('Blood Pressure', 0, 122, 70)
    skinthickness = st.sidebar.slider('Skin Thickness', 0, 100, 20)
    insulin = st.sidebar.slider('Insulin', 0, 846, 79)
    bmi = st.sidebar.slider('BMI', 0, 67, 20)
    dpf = st.sidebar.slider('Diabetes Pedigree Function', 0.0, 2.4, 0.47)
    age = st.sidebar.slider('Age', 21, 88, 33)

    user_report_data = {
        'Pregnancies': pregnancies,
        'Glucose': glucose,
        'BloodPressure': bp,
        'SkinThickness': skinthickness,
        'Insulin': insulin,
        'BMI': bmi,
        'DiabetesPedigreeFunction': dpf,
        'Age': age
    }
    report_data = pd.DataFrame(user_report_data, index=[0])
    return report_data

# Get user data
user_data = user_report()
st.subheader('Patient Data')
st.write(user_data)

# Model Tuning Section
st.title('Model Tuning')

# Sliders for hyperparameters within the main page
st.subheader('Adjust Hyperparameters:')
n_estimators = st.slider('Number of trees in the forest:', 10, 200, 50, 10)
max_depth = st.slider('Maximum depth of the tree:', 1, 20, 10, 1)

# Re-train model with new parameters
rf_tuned = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth, random_state=0)
rf_tuned.fit(x_train, y_train)

# Train model
rf = RandomForestClassifier()
rf.fit(x_train, y_train)

# Predict user data
user_result = rf.predict(user_data)

# Determine color based on prediction
color = 'blue' if user_result[0] == 0 else 'red'

# Visualizations
st.title('Visualised Patient Report')

# Age vs Pregnancies
st.header('Pregnancy count Graph (Others vs Yours)')
fig, ax = plt.subplots()
sns.scatterplot(x='Age', y='Pregnancies', data=df, hue='Outcome', palette='Greens', ax=ax)
sns.scatterplot(x=user_data['Age'], y=user_data['Pregnancies'], s=150, color=color, ax=ax)
plt.xticks(np.arange(10, 100, 5))
plt.yticks(np.arange(0, 20, 2))
plt.title('0 - Healthy & 1 - Unhealthy')
st.set_option('deprecation.showPyplotGlobalUse', False)
st.pyplot(fig)

# Age vs Glucose
st.header('Glucose Value Graph (Others vs Yours)')
ax3 = sns.scatterplot(x='Age', y='Glucose', data=df, hue='Outcome', palette='magma')
ax4 = sns.scatterplot(x=user_data['Age'], y=user_data['Glucose'], s=150, color=color)
plt.xticks(np.arange(10, 100, 5))
plt.yticks(np.arange(0, 220, 10))
plt.title('0 - Healthy & 1 - Unhealthy')
st.pyplot()

# Age vs Blood Pressure
st.header('Blood Pressure Value Graph (Others vs Yours)')
ax5 = sns.scatterplot(x='Age', y='BloodPressure', data=df, hue='Outcome', palette='Reds')
ax6 = sns.scatterplot(x=user_data['Age'], y=user_data['BloodPressure'], s=150, color=color)
plt.xticks(np.arange(10, 100, 5))
plt.yticks(np.arange(0, 130, 10))
plt.title('0 - Healthy & 1 - Unhealthy')
st.pyplot()

# Age vs Skin Thickness
st.header('Skin Thickness Value Graph (Others vs Yours)')
ax7 = sns.scatterplot(x='Age', y='SkinThickness', data=df, hue='Outcome', palette='Blues')
ax8 = sns.scatterplot(x=user_data['Age'], y=user_data['SkinThickness'], s=150, color=color)
plt.xticks(np.arange(10, 100, 5))
plt.yticks(np.arange(0, 110, 10))
plt.title('0 - Healthy & 1 - Unhealthy')
st.pyplot()

# Age vs Insulin
st.header('Insulin Value Graph (Others vs Yours)')
ax9 = sns.scatterplot(x='Age', y='Insulin', data=df, hue='Outcome', palette='rocket')
ax10 = sns.scatterplot(x=user_data['Age'], y=user_data['Insulin'], s=150, color=color)
plt.xticks(np.arange(10, 100, 5))
plt.yticks(np.arange(0, 900, 50))
plt.title('0 - Healthy & 1 - Unhealthy')
st.pyplot()

# Age vs BMI
st.header('BMI Value Graph (Others vs Yours)')
ax11 = sns.scatterplot(x='Age', y='BMI', data=df, hue='Outcome', palette='rainbow')
ax12 = sns.scatterplot(x=user_data['Age'], y=user_data['BMI'], s=150, color=color)
plt.xticks(np.arange(10, 100, 5))
plt.yticks(np.arange(0, 70, 5))
plt.title('0 - Healthy & 1 - Unhealthy')
st.pyplot()

# Age vs Diabetes Pedigree Function (DPF)
st.header('DPF Value Graph (Others vs Yours)')
ax13 = sns.scatterplot(x='Age', y='DiabetesPedigreeFunction', data=df, hue='Outcome', palette='YlOrBr')
ax14 = sns.scatterplot(x=user_data['Age'], y=user_data['DiabetesPedigreeFunction'], s=150, color=color)
plt.xticks(np.arange(10, 100, 5))
plt.yticks(np.arange(0, 3, 0.2))
plt.title('0 - Healthy & 1 - Unhealthy')
st.pyplot()

# Output
st.subheader('Your Report:')
output = 'You are not Diabetic' if user_result[0] == 0 else 'You are Diabetic'
st.title(output)

# Accuracy of original model
st.subheader('Accuracy  of Original Model:')
st.write(f"{accuracy_score(y_test, rf.predict(x_test)) * 100:.2f}%")
# Display accuracy of tuned model
st.subheader('Accuracy of Tuned Model:')
st.write(f"{accuracy_score(y_test, rf_tuned.predict(x_test)) * 100:.2f}%")

# After model training, display metrics
from sklearn.metrics import classification_report

# Predictions on test set
y_pred = rf.predict(x_test)

# Display classification report
st.subheader('Classification Report:')
st.text(classification_report(y_test, y_pred))


# Function to export report as PDF
def export_pdf_report(user_data):
    c = canvas.Canvas("diabetes_report.pdf", pagesize=letter)
    c.drawString(100, 750, "Diabetes Checkup Report")
    c.drawString(100, 730, f"Pregnancies: {user_data['Pregnancies'].values[0]}")
    c.drawString(100, 710, f"Glucose: {user_data['Glucose'].values[0]}")
    c.drawString(100, 690, f"Blood Pressure: {user_data['BloodPressure'].values[0]}")
    c.drawString(100, 670, f"Skin Thickness: {user_data['SkinThickness'].values[0]}")
    c.drawString(100, 650, f"Insulin: {user_data['Insulin'].values[0]}")
    c.drawString(100, 630, f"BMI: {user_data['BMI'].values[0]}")
    c.drawString(100, 610, f"Diabetes Pedigree Function: {user_data['DiabetesPedigreeFunction'].values[0]}")
    c.drawString(100, 590, f"Age: {user_data['Age'].values[0]}")
    c.save()

# Export PDF button
if st.button('Export PDF Report'):
    export_pdf_report(user_data)
    st.success('PDF report exported successfully!')


