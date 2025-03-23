# 🚗 City Flow - Traffic Flow Optimization

## Overview
City Flow is a data-driven project aimed at optimizing vehicle mobility in major cities across Spain. Using predictive modeling and machine learning techniques, the project analyzes traffic patterns to provide actionable insights for improving infrastructure planning and reducing congestion.

## 📂 Repository Contents
This repository contains the code, datasets, and documentation related to the City Flow project. The main components include:
- **Data preprocessing scripts**: Scripts for cleaning and merging mobility and holiday datasets.
- **Exploratory Data Analysis (EDA)**: Visualizations and statistical analyses to identify traffic patterns.
- **Predictive Models**: Implementations of various machine learning models for traffic prediction.
- **Final Model**: The optimized LightGBM-based model used for forecasting traffic flow.
- **Reports and Documentation**: Project reports, methodology, and results.

## 🔍 Project Background
### Problem Statement
The rapid increase in vehicle numbers in Spanish cities has outpaced existing road infrastructure, leading to traffic congestion. This project, in collaboration with Telefónica and UPF, aims to leverage data science to predict traffic patterns and recommend infrastructure improvements.

### Data Sources
- **Mobility Data**: Provided by Telefónica, covering vehicle movements across different provinces (2022-2024).
- **Holiday and Weather Data**: Integrated from external sources to enhance predictive accuracy.

## ⚙️ Methodology
### Data Preprocessing
- Merging mobility, holiday, and weather datasets.
- Handling missing values, duplicates, and feature engineering.

### Model Development
Several machine learning models were tested:
- **LSTM (Long Short-Term Memory Networks)**: Initially explored but found inefficient.
- **Random Forest**: Provided high accuracy but was computationally expensive.
- **LightGBM (Final Model)**: Selected for its balance between accuracy and efficiency.

### Model Performance
The final LightGBM model was trained on the top 20 provinces with the highest traffic volume. Key evaluation metrics:
- **R^2 Score**: 96.7%
- **Mean Absolute Error**: Optimized for better real-world predictions.

## 📊 Results
- Identified high-traffic periods and seasonal patterns.
- Forecasted traffic trends for the next three months.
- Provided insights into which factors most influence vehicle movement, including holidays and weather conditions.

## 🌐 Streamlit Web App
A **Streamlit-based web application** is included in this repository to provide an interactive visualization of traffic predictions. Users can upload datasets, view insights, and explore forecasted traffic trends.

### Running the Web App
To start the Streamlit app, run the following command:
```sh
streamlit run Home.py
```
This will launch a browser interface where you can interact with the model's predictions in real-time.

## 🚀 Getting Started
### Prerequisites
- Python 3.8+
- Required libraries: `pandas`, `numpy`, `scikit-learn`, `lightgbm`, `matplotlib`, `seaborn`

### Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/uzairrp/Mob_optimization.git
   ```
2. Navigate to the directory:
   ```sh
   cd Mob_optimization
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

### Running the Project
- Execute data preprocessing:
  ```sh
  python preprocess.py
  ```
- Train the LightGBM model:
  ```sh
  python train_model.py
  ```
- Generate predictions:
  ```sh
  python predict.py
  ```

## 👥 Contributors
- **Project Manager**: Uzair Ramzan
- **Team Members**: Marc Bacaicoa, Marc Riera, Eneko Treviño, Ricard Segura
- **Stakeholders**: Telefónica, UPF

## 📜 License
This project is licensed under the MIT License.

---
For any questions or contributions, feel free to raise an issue or submit a pull request! 🚦

