
import streamlit

streamlit.title('My Parents New Healthy Diner')

streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach and Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index))

# afficher la liste selectionnee
streamlit.dataframe(my_fruit_list)


#recette de base pour les clients
fruits_selected = streamlit.multiselect("Pick some fruits:",list(my_fruit_list.index),['Banana','Honeydew','Kiwifruit'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

#afficher le tableau des fruits selectionnes
streamlit.dataframe(fruits_to_show)



# 20/03/2023
# nouvelle section avec fruityvice
streamlit.header("Fruityvice Fruit Advice!")
fruit_choice = streamlit.text_input('Tu veux des infos sur quel fruit?','Kiwi')
streamlit.write('Le user a choisi',fruit_choice)

import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)



# dessous, ca normalise le texte qui est dans la reponse fruityvice
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# ca affiche un tableau
streamlit.dataframe(fruityvice_normalized)


import snowflake.connector

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from fruit_load_list")
my_data_row = my_cur.fetchone()
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_row)
