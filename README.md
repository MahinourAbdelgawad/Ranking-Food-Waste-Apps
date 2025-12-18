# 🍏 EcoMarketplace: The Food Waste Reduction Simulator

Welcome to the **EcoMarketplace** repository! This project is a modular simulation environment designed to bridge the gap between local food businesses and eco-conscious customers. Our goal is to reduce environmental impact while creating a sustainable, profitable marketplace for "Surprise Bags."

---

## 📖 1. Introduction
EcoMarketplace is a comprehensive program that simulates a dynamic food-waste ecosystem. 
* **The Goal:** Connect local businesses with surplus inventory to hungry customers looking for high-quality meals at a discount.
* **The Solution:** By turning potential waste into "Surprise Bags," we help businesses reclaim lost revenue, satisfy community demand, and significantly reduce the environmental footprint of thrown-away food.

---

## ⚠️ 2. The Problem
Managing daily food surplus is a major challenge due to unpredictable demand. This leads to three critical failures:
* **The Business Problem:** Stores lose significant revenue on unsold, perfectly good inventory.
* **The Environmental Problem:** Food waste is a primary driver of global CO2 emissions.
* **The Satisfaction Problem:** Traditional recommendation systems often fail to match the right bag to the right customer, leading to lost trust and high churn rates.

**Our Mission:** Develop an algorithm that finds the **local optimal solution**—balancing profit, waste reduction, and customer happiness.

---

## ⚙️ 3. Our Program
The project is built as a modular simulation environment to test and validate different marketplace strategies.

### 🏗️ Core Components
* **Simulator:** The central engine that manages daily cycles, tracks inventory across multiple days, and handles the "matching" logic.
* **Store & Customer Objects:** Detailed data models that track geographic location (Lat/Long), real-time ratings, and personalized customer valuation profiles.
* **Algorithm Suite:** A collection of different recommendation strategies, including:
  * `Greedy Baseline`: A simple "top-rated" sorter used as a benchmark.
  * `Hybrid Optimization Algorithm`: Our advanced multi-variable solution.

---

## 🧪 4. Development of the Main Algorithm
Our "Final Algorithm" wasn't built overnight. It was the result of an iterative, data-driven brainstorming process by our 4-member team:

1.  **Brainstorming:** Each member developed a distinct algorithmic approach to solve the "Marketplace Balance" problem.
2.  **Simulation Stress-Testing:** All 4 algorithms were run through identical simulation cycles to ensure a fair comparison.
3.  **Data Visualization:** We analyzed the results through performance graphs, focusing on **Revenue Efficiency** and **Waste Reduction**.
4.  **The Combination:** We identified the top two performing strategies and merged them into a single, robust hybrid engine.



---

## ✅ 5. The Solution: The Final Hybrid Algorithm
The resulting algorithm brings together **personalization, general quality, and exploration** into one balanced decision-making process.

### Key Features:
* **Loyalty & Personalization:** Prioritizes stores that a specific customer has enjoyed in the past.
* **Practical Factors:** Real-time scoring based on price, rating, distance, and current availability.
* **The Exploration Engine:** Deliberately introduces new or unfamiliar stores to the user’s feed. This prevents "recommendation bubbles" and ensures that small or new businesses get a fair chance to succeed.
* **Adaptability:** By scoring stores from multiple perspectives, the algorithm remains fair and relevant across different urban environments and customer types.

---

## 🛠 Tech Stack
* **Python 3.x**
* **Dynamic Programming (Selection Logic)**
* **Matplotlib/Seaborn (Data Visualization)**
* **Object-Oriented Programming (Store/Customer Models)**

---


## 📓 6. How to Run (Jupyter Notebook)

The simulation is best experienced in a Jupyter Notebook environment, which allows for real-time visualization of the marketplace dynamics and algorithm performance.

⚙️ Prerequisites

It can simply be ran on google colab, however make sure to have the files for store and customer data uploaded in a 'datasets' to avoid issues with finding filepath.



