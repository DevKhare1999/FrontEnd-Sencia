import streamlit as st
import psycopg2
import requests
import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# API base URL
BASE_URL = os.getenv('BACKEND_URL')

# Authentication state
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "auth_token" not in st.session_state:
    st.session_state["auth_token"] = None
if "username" not in st.session_state:
    st.session_state["username"] = None

# Authentication functions
def login(username, password):
    """Send login request to backend and return success or failure."""
    response = requests.post(
        f"{BASE_URL}/login",
        headers={"Content-Type": "application/json"},
        json={"username": username, "password": password}
    )
    if response.status_code == 200:
        data = response.json()
        st.session_state["logged_in"] = True
        st.session_state["auth_token"] = data.get("token")
        st.session_state["username"] = username
        return True
    else:
        st.error("Invalid credentials. Please try again.")
        return False

def signup(username, password):
    """Send signup request to backend."""
    response = requests.post(
        f"{BASE_URL}/signup",
        headers={"Content-Type": "application/json"},
        json={"username": username, "password": password}
    )
    if response.status_code == 201:
        st.success("Signup successful! You can now log in.")
    elif response.status_code == 400:
        st.error("Username already exists. Please choose a different username.")
    else:
        st.error("An error occurred. Please try again.")

def logout():
    """Log the user out."""
    st.session_state["logged_in"] = False
    st.session_state["auth_token"] = None
    st.session_state["username"] = None
    st.success("You have been logged out.")

# Fetch agents from the backend server
def fetch_agents():
    response = requests.get(
        f"{BASE_URL}/agents",
        headers={"Authorization": f"{st.session_state['auth_token']}"}
    )
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch agents.")
        return []

# Save a new agent to the backend server
def save_agent(agent_name, prompt, image_url="image_placeholder.png"):
    data = {
        "agent_name": agent_name,
        "prompt": prompt,
        "image_url": image_url
    }
    response = requests.post(
        f"{BASE_URL}/agents",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"{st.session_state['auth_token']}"
        },
        json=data
    )
    if response.status_code == 200:
        st.success("Agent saved successfully")
    else:
        st.error("Failed to save agent")

# Save a new product to the backend server
def save_product(name, price, description):
    data = {
        "name": name,
        "price": price,
        "description": description
    }
    response = requests.post(
        f"{BASE_URL}/products",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"{st.session_state['auth_token']}"
        },
        json=data
    )
    if response.status_code == 200:
        st.success("Product saved successfully")
    else:
        st.error("Failed to save product")

# Home Page - Display available agents
def home_page():
    st.title("Available Agents")
    st.write(f"Welcome, {st.session_state['username']}!")
    st.write("Here are the agents available for use:")
    agents = fetch_agents()
    for agent_name, prompt, image_url in agents:
        st.image(image_url, width=150, caption=agent_name)
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

# Product Management Page with Embed JS
def product_page():
    st.title("Product Management and Embed JavaScript")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("Add new product details manually (for testing):")
        product_name = st.text_input("Product Name")
        product_price = st.text_input("Price")
        product_desc = st.text_area("Description")
        if st.button("Save Product"):
            # Save product to database logic can go here
            save_product(product_name, product_price, product_desc)
            st.success(f"Product '{product_name}' saved!")
    
    with col2:
        st.write("Generate an embeddable script to send web URLs to the Flask backend.")
        js_url = st.text_input("Enter Web URL")
        if st.button("Generate Embed Code"):
            response = requests.post(
                os.getenv('BACKEND_URL')+"/analyze",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"{st.session_state['auth_token']}"
                },
                json={"url": js_url}
            )
            if response.status_code == 200:
                st.write("Analysis successful!")
                output = response.json()
                embed_code = '''// Embeddable JavaScript Boilerplate for Displaying JSON Data
(function () {
// Create a container for the product display
const containerId = "product-display-container";

// Create or find the container element on the page
let container = document.getElementById(containerId);
if (!container) {
    container = document.createElement("div");
    container.id = containerId;
    document.body.appendChild(container);
}

// Sample JSON Data for a single product (Replace this with dynamic data fetching as needed)
const product = {''' + f'''
    name: "{output['name']}",
    price: "{output['price']}",
    description: "{output['description']}"
''' +'''};

// Function to render product data into HTML
function renderProduct(product) {
    // Clear existing content
    container.innerHTML = "";

    // Create a header for the container
    const header = document.createElement("h2");
    header.textContent = "Product Details";
    container.appendChild(header);

    // Generate HTML for the product
    const productCard = document.createElement("div");
    productCard.style.border = "1px solid #ccc";
    productCard.style.padding = "10px";
    productCard.style.margin = "10px 0";
    productCard.style.borderRadius = "5px";

    const productName = document.createElement("h3");
    productName.textContent = product.name;
    productCard.appendChild(productName);

    const productPrice = document.createElement("p");
    productPrice.textContent = `Price: ${product.price}`;
    productCard.appendChild(productPrice);

    const productDescription = document.createElement("p");
    productDescription.textContent = `Description: ${product.description}`;
    productCard.appendChild(productDescription);

    container.appendChild(productCard);
}

// Render the sample product (replace this with fetched data if needed)
renderProduct(product);
})();'''
                st.session_state.embed_code = embed_code
            else:
                st.write("Failed to analyze the URL.")

    if 'embed_code' in st.session_state:
        st.write("Last generated embed code:")
        st.code(st.session_state.embed_code, language="javascript")

# Login Page
def login_page():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if login(username, password):
            st.success(f"Welcome, {username}!")

# Signup Page
def signup_page():
    st.title("Signup")
    username = st.text_input("Choose a Username")
    password = st.text_input("Choose a Password", type="password")
    if st.button("Signup"):
        signup(username, password)

# Main App
def main():
    if not st.session_state["logged_in"]:
        menu = st.sidebar.radio("Choose an option", ["Login", "Signup"])
        if menu == "Login":
            login_page()
        elif menu == "Signup":
            signup_page()
    else:
        st.sidebar.title(f"Welcome, {st.session_state['username']}")
        if st.sidebar.button("Logout"):
            logout()
        menu = st.sidebar.radio("Navigate", ["Home", "Agents", "Products"])
        if menu == "Home":
            home_page()
        elif menu == "Agents":
            agent_page()
        elif menu == "Products":
            product_page()

if __name__ == "__main__":
    main()