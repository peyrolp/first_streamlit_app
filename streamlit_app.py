
import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Parents New Healthy Diner')

streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach and Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

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
# 21/03/2023
# nouvelle section avec fruityvice
# creation d'une fonction pour afficher les infos venant de fruityvice
def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized
  
  
streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('Tu veux des infos sur quel fruit?')
  if not fruit_choice:
    streamlit.error("Please choisis un fruit pour avoir des infos")
  else:
    back_from_function = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(back_from_function)
except URLError as e:
  streamlit.error()
  
# dessous, ca normalise le texte qui est dans la reponse fruityvice
# ca affiche un tableau


################################################
#streamlit.stop()


streamlit.header("The fruit load list contains:")
#snowflake related functions
def get_fruit_load_list():
       with my_cnx.cursor() as my_cur:
            my_cur.execute("select * from fruit_load_list")
            return my_cur.fetchall()

# ajout d'(un bouton pour charger les fruits
if streamlit.button('Charge les fruits !'):
        my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
        my_data_rows = get_fruit_load_list()
        streamlit.dataframe(my_data_rows)
        
#streamlit.stop()

#

#autoriser l'ajout d'un fruit
def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
         my_cur.execute("insert into fruit_load_list values ("new_fruit") ")
         return "Thanks for adding " + new_fruit
    
add_my_fruit= streamlit.text_input('Quel fruit ajouter dans la liste ?')
if streamlit.button('Add a fruit dans la liste'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    back_from_function = insert_row_snowflake(add_my_fruit)
    streamlit.text(back_from_function)


