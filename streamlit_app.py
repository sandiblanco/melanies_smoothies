# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas as pd

# Write directly to the app
st.title(f"Customize your smoothie :cup_with_straw: {st.__version__}")
st.write(
  """Choose the fruits you want in your smoothie!
  """
)

name_on_order = st.text_input("Name on smoothie")
st.write(
  """The name on your smoothie will be: 
  """, name_on_order
)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))
st.dataframe(data=my_dataframe, use_container_width=True)
st.stop()

ingredients_list = st.multiselect('Choose up to 5 ingredientes:', my_dataframe, max_selections=5)

if ingredients_list:
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen+' '
        st.subheader(fruit_chosen + ' Nutrition information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
        sf_df= st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
    
    #st.write(ingredients_string)
    
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
                values ('""" + ingredients_string + """','""" + name_on_order + """')"""
    
    time_to_insert = st.button('Submit Order')
    
    st.write(my_insert_stmt)
    st.stop
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
      

