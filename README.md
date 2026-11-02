# Data Analysis Dashboard

An interactive data analysis web application built with **Streamlit**, **Pandas**, and **Plotly**, fully containerized using **Docker** and **Docker Compose**.

---

## 🌟 Features

- **Interactive Filters:** Filter dataset by city or fruit type dynamically.
- **KPI Metrics:** Overview of Total Units Sold, Total Revenue, Average Unit Price, and Top Selling Fruit.
- **Visualizations (Plotly):**
  - Interactive Bar Chart: Units sold per City by Fruit type.
  - Donut Chart: Market share distribution by revenue.
  - Line Chart: Revenue trends over time.
- **Data Exploration:** Interactive data table with CSV export capability and descriptive statistics.

---

## 📁 Project Structure

```
Docker/
├── app.py                # Main Streamlit dashboard application
├── requirements.txt      # Python dependencies
├── Dockerfile            # Container definition
├── docker-compose.yml    # Orchestration configuration
└── README.md             # Documentation
```

---

## 🚀 Getting Started

### Option 1: Running with Docker (Recommended)

1. Make sure **Docker** and **Docker Compose** are installed and running on your machine.
2. Open a terminal in the project directory and start the container:

```bash
docker compose up --build
```
*(or `docker-compose up --build` on older Compose versions)*

3. Open your browser and navigate to:
```text
http://localhost:8501
```

To stop the container:
```bash
docker compose down
```

---

### Option 2: Running Locally (Python Environment)

1. Ensure Python 3.9+ is installed.
2. Install the required dependencies:
```bash
pip install -r requirements.txt
```
3. Run the Streamlit app:
```bash
streamlit run app.py
```
4. Access the dashboard in your browser at `http://localhost:8501`.
