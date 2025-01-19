# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas

# Write directly to the app
st.title("Example Streamlit App :cup_with_straw:")
st.write(
    """Replace this example with your own code!
    **And if you're new to Streamlit,** check
    out our easy-to-follow guides at
    [docs.streamlit.io](https://docs.streamlit.io).
    """
)

cnk = st.connection("snowflake")
session = cnk.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"), col("SEARCH_ON"))
pd_df = my_dataframe.to_pandas()
st.dataframe(pd_df)

st.stop()

ingredients_list = st.multiselect(
    "Select some items",
    my_dataframe,
    max_selections=5
)

name_on_order = st.text_input("Name on smoothie")
st.write("The name on order is " + name_on_order)

time_to_insert = st.button("Submit Order")

if ingredients_list:
    ingredients_string = ''
    for item in ingredients_list:
        ingredients_string += item + ' '

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,NAME_ON_ORDER)
        values ('""" + ingredients_string + """', '""" + name_on_order + """')"""
  
    #st.write(my_insert_stmt)
    search_on = pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
    st.write('The search value for ', fruit_chosen,' is ', search_on, '.')

    st.subheader(item + ' Nutrition Information')
    smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + search_on)
    sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width = True)
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered, ' + name_on_order + '!', icon="✅")

