import streamlit as st
import pandas
import random
import numpy as np
from scipy.optimize import minimize

df=pandas.read_csv("finaldsgpt4.csv_Dallas.csv")
df2=pandas.DataFrame()
df2["Food Item"]=df["item_name"]







def calculate_explicit_utility(proteins_rank, minerals_rank, vitamins_rank, carbohydrates_rank, fats_rank, fibers_rank, sugars_rank,calories_rank,user_calorie,goal):
    
    # Define mapping of rankings to weights
    ranking_weights = {'Low': 1, 'Medium': 2, 'High': 3}
    if goal=="Lose weight":
        weights = {'Proteins': 3, 'Minerals': 2, 'Vitamins': 2, 'Carbohydrates': 1, 'Fats': 1, 'Fibers': 3, 'Sugars': 1}
        calorie=user_calorie-100
    elif goal=="Maintain weight":
        weights = {'Proteins': 2.5, 'Minerals': 2, 'Vitamins': 2, 'Carbohydrates': 2, 'Fats': 2, 'Fibers': 3, 'Sugars': 1}
        calorie=user_calorie
    elif goal=="Gain weight":
        weights = {'Proteins': 3, 'Minerals': 2.5, 'Vitamins': 2.5, 'Carbohydrates': 2.5, 'Fats': 2.5, 'Fibers': 1.5, 'Sugars': 2}
        calorie=user_calorie+100

    # Calculate scores for each nutrient category
    scores = {'Proteins': weights['Proteins']-ranking_weights[proteins_rank] >0,
              'Minerals': (ranking_weights[minerals_rank] - weights['Minerals']) if -ranking_weights[minerals_rank] + weights['Minerals'] > 0 else 1.2*(ranking_weights[minerals_rank] - weights['Minerals']),
              'Vitamins': (-ranking_weights[vitamins_rank] + weights['Vitamins']) if -ranking_weights[vitamins_rank] + weights['Vitamins'] > 0 else 0.8*(-ranking_weights[vitamins_rank] + weights['Vitamins']),
              'Carbohydrates': (-ranking_weights[carbohydrates_rank] + weights['Carbohydrates']) if -ranking_weights[carbohydrates_rank] + weights['Carbohydrates'] > 0 else (-ranking_weights[carbohydrates_rank] + weights['Carbohydrates'])**2,
              'Fats': (-ranking_weights[fats_rank] + weights['Fats']) if -ranking_weights[fats_rank] + weights['Fats'] > 0 else (-ranking_weights[fats_rank] + weights['Fats'])**2,
              'Fibers': (-ranking_weights[fibers_rank] + weights['Fibers']),
              'Sugars': (-ranking_weights[sugars_rank] + weights['Sugars']) if -ranking_weights[sugars_rank] + weights['Sugars'] > 0 else (-ranking_weights[sugars_rank] + weights['Sugars'])**2,
              'calories': (-calories_rank + calorie)/100 if -calories_rank + calorie > 0 else (-calories_rank/100 + calorie/100)*-0.8}
    utility_score = sum(scores.values())
    return utility_score


activity={"Sedentary (little or no exercise)":1.16826132, "Lightly active (exercise 1–3 days/week)":1.28784451, "Active (exercise 6–7 days/week)":1.40727724,"Very active (hard exercise 6–7 days/week)":1.63663733}
st.title('Calorie Calculator')
def validate_input(weight,height,age,sex,activity):
    if not height:
        st.warning("Please enter your height.")
        return False
    if not weight:
        st.warning("Please enter your weight.")
        return False
    if not age:
        st.warning("Please enter your age.")
        return False
    if not sex:
        st.warning("Please select your sex.")
        return False
    if not activity:
        st.warning("Please select your activity level.")
        return False
    if age < 0 or age > 150:
        st.warning("Please enter a valid age between 0 and 150.")
        return False
    return True


with st.form(key='form1',clear_on_submit=True):
    st.subheader("About you")
    Sex= st.radio("Select an option",["Male","Female"], horizontal=True, label_visibility="hidden")
    height = st.number_input("Height", placeholder="in cm",value=None)
    weight = st.number_input("Weight", placeholder="in kg",value=None)
    age = st.number_input("Age", placeholder="in years",value=None)
    st.subheader("How active are you?")
    option = st.radio("Select an option", ["Sedentary (little or no exercise)", "Lightly active (exercise 1–3 days/week)","Active (exercise 6–7 days/week)", "Very active (hard exercise 6–7 days/week)"])
    goals= st.radio("Select an option", ["Lose weight","Maintain weight","Gain weight"])
    calculate= st.form_submit_button("Calculate")
if calculate:
    if validate_input(weight,height,age,Sex,option):
        if Sex=="Female":
                BMR = 668.19296854+ (9.93930012*int(weight)) + (1.86102009*int(height)) - (4.78038547*int(age)) 
                AMR = BMR*activity[option]
                AMRP=(AMR-200)/3
                st.success("On a 3 meal scale, you should take "+str(round(AMRP))+"cal per meal with 200 calories for throughout the day snacking")
                st.write("Your Basal Metabolic Rate is",round(BMR))
                st.write("Your Active Metabolic Rate is",round(AMR))
                
        

        else:
                BMR = 21.77589707 + (13.85398532*int(weight)) + (5.49432274*int(height)) - (6.875253*int(age))
                AMR = BMR*activity[option]
                AMRP=(AMR-200)/3
                st.success("On a 3 meal scale, you should take "+str(round(AMRP))+" cal per meal with 200 calories for throughout the day snacking")
                st.write("Your Basal Metabolic Rate is",round(BMR))
                st.write("Your Active Metabolic Rate is",round(AMR))
                
        explicit_dietry_utility=[]

        for i in range(0, len(df)):
            utility_score = calculate_explicit_utility(df.iloc[i]['Proteins'], df.iloc[i]['Minerals'], df.iloc[i]['Vitamins'], df.iloc[i]['Carbohydrates'], df.iloc[i]['Fats'], df.iloc[i]['Fibers'], df.iloc[i]['Sugars'],df.iloc[i]['Calories'],AMRP,goals)
            explicit_dietry_utility.append(utility_score)
        df2['Explicit Dietry Utility'] = explicit_dietry_utility
        ratings_utility = []
        for i in range(0,len(df)):
            ratings_utility.append(5-df["score"].iloc[i])
        df2["Ratings Utility"] = ratings_utility
        price_utility=[]
        for i in range(0,len(df)):
            price_utility.append(float(df["price"].iloc[i][:-4])/10)
        df2["Price Utility"] = price_utility
        df2["Primary Flavour"]=df["Primary_Flavour"]
        df2["Secondary Flavour"]=df["Secondary_Flavour"]
        df2["Dish_type"]=df["Dish_type"]
        ts = [round(random.uniform(1, 4), 1) for _ in range(len(df2))]
        df2["Time spent"]=ts
        tsma=df2["Time spent"].max()
        tsmi=df2["Time spent"].min()
        tsu=[]
        for i in range(0,len(df2)):
            tsu.append((round((df2["Time spent"].iloc[i]-tsmi)/(tsma-tsmi),2)))
        df2["Time Spent Utility"]=tsu
        
        df2['restaurant_name']=df['restaurant_name']
        sampled_df = df2.sample(n=50)
        freq_utility={}
        freq_list=sampled_df["Primary Flavour"].value_counts()
        freq_list.to_dict()
        for k in freq_list.keys():
            freq_utility[k]=round((freq_list[k]-min(freq_list.values))/(max(freq_list.values)-min(freq_list.values)),2)
        freq_list2=sampled_df["Secondary Flavour"].value_counts()
        freq_list2.to_dict()
        freq_utility2={}
        for k in freq_list2.keys():
            freq_utility2[k]=round((freq_list2[k]-min(freq_list2.values))/(max(freq_list2.values)-min(freq_list2.values)),2)
        iu1=[]
        iu2=[]
        for i in range(0,len(df2)):
            if df2["Primary Flavour"].iloc[i] in freq_utility.keys():
                iu1.append(freq_utility[df2["Primary Flavour"].iloc[i]])
            else:
                iu1.append(0)
            if df2["Secondary Flavour"].iloc[i] in freq_utility2.keys():
                iu2.append(freq_utility2[df2["Secondary Flavour"].iloc[i]])
            else:
                iu2.append(0)
        df2["Implicit Utility 1"]=iu1
        df2["Implicit Utility 2"]=iu2
        sampled_df = pandas.merge(sampled_df, df2, on='Food Item', how='inner')
        sampled_df=sampled_df.iloc[:, 0:11]
        def objective(weights):
            fs = 0
            for i in range(len(df2)):
                s = 0
                for j in range(2):
                    if j == 0:
                        s += (df2["Time Spent Utility"].iloc[i] - df2["Implicit Utility 1"].iloc[i] * weights[j]) ** 2
                    elif j == 1:
                        s += (df2["Time Spent Utility"].iloc[i] - df2["Implicit Utility 2"].iloc[i] * weights[j]) ** 2
                fs += s
            return fs
        def constraint(weights):
            return 1 - np.sum(weights)

        w0=[0.5,0.5]
        objective(w0)
        bound=(0,1)
        bnd=[bound,bound]
        con={"type":"eq","fun":constraint}
        sol=minimize(objective,w0,method="SLSQP",bounds=bnd,constraints=con)
        weights=sol.x.tolist()
        df2["Final Implicit utility"]=1-(df2["Implicit Utility 1"]*weights[0]+df2["Implicit Utility 2"]*weights[1])
        df2["Final Utility"]=round(df2["Explicit Dietry Utility"]/8)+df2["Ratings Utility"]+df2["Price Utility"]+df2["Final Implicit utility"]
        df2.sort_values(by="Final Utility",ascending=True,inplace=True)
        st.write(df2.head())

