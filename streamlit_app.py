# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

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
my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"))

#st.dataframe(data=my_dataframe, use_container_width=True)

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

    #st.write(ingredients_string)
    #my_insert_stmt = """ insert into smoothies.public.orders(ingredients)
    #        values ('""" + ingredients_string + """')"""

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,NAME_ON_ORDER)
        values ('""" + ingredients_string + """', '""" + name_on_order + """')"""
        
    
    
    st.write(my_insert_stmt)
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered, ' + name_on_order + '!', icon="✅")
    
