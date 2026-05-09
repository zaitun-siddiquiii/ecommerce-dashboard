# E-Commerce Sales Dashboard

> A complete data science project: data cleaning, SQL analysis,
> customer segmentation, and interactive Streamlit dashboard.

## Project Summary
Analysed 128,000+ e-commerce transactions to uncover revenue trends,
top-performing products, regional performance, and customer segments.

## Tools Used
- Python 3.11 (pandas, numpy, matplotlib, seaborn, plotly)
- SQLite (via Python sqlite3)
- scikit-learn (RFM segmentation)
- Streamlit (streamlit)
- Jupyter Notebook

## Project Structure
```
ecommerce-dashboard/
├── notebooks/     # Jupyter notebooks (EDA, SQL, RFM)
├── sql/           # SQL queries file
├── data/cleaned/  # Cleaned CSV files
├── outputs/       # Saved chart images
├── app.py         # Streamlit dashboard (Python)
└── README.md
```

## Key Findings
- Electronics category accounts for 38% of total revenue
- Friday and Saturday are peak order days
- 22% of customers are "Champions" — they drive 51% of revenue
- Q4 shows 28% higher revenue vs Q1 (holiday effect)

## How to Run
1. Clone the repo: `git clone <url>`
2. Install dependencies: `pip install -r requirements.txt`
3. Download dataset from Kaggle and place in `data/raw/`
4. Run notebooks in order: 01 → 02 → 03 → 04
5. Run the Streamlit dashboard: `streamlit run app.py`

## Dataset
Source: Kaggle — E-Commerce Sales Dataset by thedevastator
