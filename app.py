import streamlit as st
# import psycopg2

# Configure PostgreSQL connection (replace with your credentials)
# def get_db_connection():
#     return psycopg2.connect(
#         host="your_host",
#         database="your_database",
#         user="your_user",
#         password="your_password"
#     )

# Login page
def login():
    st.title("Login Page")
    st.text_input("Username", key="username")
    st.text_input("Password", type="password", key="password")
    if st.button("Login"):
        st.session_state.logged_in = True

# Dashboard
def dashboard():
    st.sidebar.title("Dashboard")
    menu = st.sidebar.radio("Menu", ["Agent", "Products", "Embed JS", "View My Website"])

    # Agent Management
    if menu == "Agent":
        st.header("Agent Management")
        agent_name = st.text_input("Agent Name")
        agent_prompt = st.text_input("Agent Prompt")
        if st.button("Create New"):
            st.success(f"Agent {agent_name} created!")

    # Product Management
    elif menu == "Products":
        st.header("Product Management")
        st.write("Add New Product:")
        product_name = st.text_input("Product Name")
        product_price = st.text_input("Price")
        product_desc = st.text_area("Description")
        if st.button("Save"):
            st.success(f"Product {product_name} saved!")

    # Embed JS
    elif menu == "Embed JS":
        st.header("Embed JavaScript")
        js_url = st.text_input("Enter JS Script URL")
        if st.button("Generate Embed Code"):
            embed_code = f"<script src='{js_url}'></script>"
            st.code(embed_code)

    # View My Website
    elif menu == "View My Website":
        st.header("My Website")
        st.write("This is a placeholder for your website preview.")

# Main App
def main():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        login()
    else:
        dashboard()

if __name__ == "__main__":
    main()
