# 🍏 EcoMarketplace: The Food Waste Reduction Simulator

Welcome to the **EcoMarketplace** repository! This project is a modular simulation environment designed to bridge the gap between local food businesses and eco-conscious customers. Our goal is to reduce environmental impact while creating a sustainable, profitable marketplace for "Surprise Bags."

---

## 🔗 GitHub Repository Link
https://github.com/MahinourAbdelgawad/Ranking-Food-Waste-Apps

---

## 📖 1. Introduction
EcoMarketplace is a comprehensive program that simulates a dynamic food-waste ecosystem.  

- **The Goal:** Connect local businesses with surplus inventory to hungry customers looking for high-quality meals at a discount.  
- **The Solution:** By turning potential waste into "Surprise Bags," we help businesses reclaim lost revenue, satisfy community demand, and significantly reduce the environmental footprint of thrown-away food.

---

## ⚠️ 2. The Problem
Managing daily food surplus is a major challenge due to unpredictable demand. This leads to three critical failures:

- **The Business Problem:** Stores lose significant revenue on unsold, perfectly good inventory.  
- **The Environmental Problem:** Food waste is a primary driver of global CO₂ emissions.  
- **The Satisfaction Problem:** Traditional recommendation systems often fail to match the right bag to the right customer, leading to lost trust and high churn rates.

**Our Mission:** Develop an algorithm that finds the **local optimal solution**—balancing profit, waste reduction, and customer happiness.

---

## ⚙️ 3. Our Program
The project is built as a modular simulation environment to test and validate different marketplace strategies.

### 🏗️ Core Components
- **Simulator:** The central engine that manages daily cycles, tracks inventory across multiple days, and handles the matching logic.  
- **Store & Customer Objects:** Data models that track geographic location (latitude/longitude), ratings, and personalized customer valuation profiles.  
- **Algorithm Suite:** A collection of recommendation strategies, including:
  - `Greedy Baseline`: A simple top-rated sorter used as a benchmark.
  - `Hybrid Optimization Algorithm`: Our advanced multi-variable solution.

---

## 🧪 4. Development of the Main Algorithm
Our final algorithm was developed through an iterative and data-driven process by our four-member team:

1. **Brainstorming:** Each member proposed a distinct algorithmic approach to solve the marketplace balance problem.  
2. **Simulation Stress-Testing:** All algorithms were tested under identical simulation conditions for fair comparison.  
3. **Data Visualization:** Performance was analyzed using graphs focused on **revenue efficiency** and **food waste reduction**.  
4. **Combination:** The two best-performing strategies were merged into a single hybrid solution.

---

## ✅ 5. The Solution: The Final Hybrid Algorithm
The final algorithm combines **personalization**, **general quality**, and **exploration** into one balanced recommendation strategy.

### Key Features
- **Loyalty & Personalization:** Prioritizes stores a customer has enjoyed previously.  
- **Practical Factors:** Considers price, rating, distance, and current bag availability.  
- **Exploration Engine:** Introduces new or less familiar stores to avoid recommendation bubbles and support smaller businesses.  
- **Adaptability:** Performs well across different customer types and urban settings.

---

## 🛠 Tech Stack
- **Python 3.x**
- **Dynamic Programming (Selection Logic)**
- **Matplotlib / Seaborn (Data Visualization)**
- **Object-Oriented Programming (Store & Customer Models)**

---

## 📓 6. How to Run (Jupyter Notebook)

The simulation is best experienced in a **Jupyter Notebook**, which allows for step-by-step execution and visualization of marketplace dynamics.

### ⚙️ Prerequisites
- The notebook can be run on **Google Colab**.
- Make sure the store and customer files are uploaded inside a folder named `datasets/` to avoid file path issues.

---

## 📊 7. How to Run the Dashboard (Admin Analytics)

A separate **admin analytics dashboard** is included to visualize food-waste potential, customer satisfaction, and recommendation behavior.  
The dashboard is located in a separate folder and reads directly from the same `datasets/` directory.

### 📁 Folder Structure (Important)
dashboard/
app.py
datasets/
storesX.csv
customersX.csv
As long as the `datasets/` folder exists and contains matching `storesX.csv` and `customersX.csv` files, the dashboard will run without any modifications.

---

### ✅ Running the Dashboard Locally (VS Code / Terminal)

1. **Navigate to the project root directory**
```bash
cd Ranking-Food-Waste-Apps

Create and activate a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate


 Install the required packages

 pip install streamlit pandas plotly folium streamlit-folium

Run the dashboard

streamlit run dashboard/app.py

Once the dashboard is running, a browser window will open automatically. From there, you can:

Switch between datasets

View food-waste potential (bags @ 9AM) and satisfaction metrics

Explore store locations on an interactive map

Inspect recommendations for individual customers
