import streamlit as st
import psycopg2
import requests
import os

# Function to connect to the database

# PostgreSQL connection (replace with your credentials)
def get_db_connection():
    return psycopg2.connect(
        host="dpg-ctc1nsggph6c73aa1qpg-a.oregon-postgres.render.com",
        database="sencia",
        user="sencia_user",
        password="PAkNnlSC9WNSc4rafBNcyifVulbgLjqv"
    )

# Fetch agents from the database
def fetch_agents():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT agent_name, prompt, image_url FROM agents")
    agents = cur.fetchall()
    conn.close()
    return agents

# Save a new agent to the database
def save_agent(agent_name, prompt, image_url="image_placeholder.png"):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO agents (agent_name, prompt, image_url) VALUES (%s, %s, %s)",
                (agent_name, prompt, image_url))
    conn.commit()
    conn.close()

# Home Page - Display available agents
def home_page():
    st.title("Available Agents")
    st.write("Here are the agents available for use:")
    agents = fetch_agents()
    for agent_name, prompt, image_url in agents:
        if not os.path.isabs(image_url):
            image_url = os.path.join(os.path.dirname(__file__), image_url)
        if os.path.exists(image_url):
            st.image(image_url, width=150, caption=agent_name)
        else:
            st.image("https://via.placeholder.com/150", width=150, caption=agent_name)
        st.write(f"**Prompt:** {prompt}")
        st.divider()

# Agent Management Page
def agent_page():
    st.title("Agent Management")
    st.write("Add a new agent:")
    agent_name = st.text_input("Agent Name")
    prompt = st.text_input("Agent Prompt")
    image_url = st.text_input("Agent Image URL (optional)", value="image_placeholder.png")
    if st.button("Add Agent"):
        save_agent(agent_name, prompt, image_url)
        st.success(f"Agent '{agent_name}' added!")

# Embed JS for Web URL Processing
def embed_js_page():
    st.title("Embed JavaScript")
    st.write("Generate an embeddable script to send web URLs to the Flask backend.")
    js_url = st.text_input("Enter Web URL")
    if st.button("Generate Embed Code"):
        embed_code = f"<script src='{js_url}'></script>"
        st.code(embed_code)

# Product Management Page (Optional)
def product_page():
    st.title("Product Management")
    st.write("Add new product details manually (for testing):")
    product_name = st.text_input("Product Name")
    product_price = st.text_input("Price")
    product_desc = st.text_area("Description")
    if st.button("Save Product"):
        # Save product to database logic can go here
        st.success(f"Product '{product_name}' saved!")

# Main App
def main():
    st.sidebar.title("Menu")
    menu = st.sidebar.radio("Navigate", ["Home", "Agents", "Embed JS", "Products"])

    if menu == "Home":
        home_page()
    elif menu == "Agents":
        agent_page()
    elif menu == "Embed JS":
        embed_js_page()
    elif menu == "Products":
        product_page()

if __name__ == "__main__":
    main()
