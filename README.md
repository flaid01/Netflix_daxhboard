# Netflix Content Dashboard

A data engineering project that builds an end-to-end analytics pipeline on Netflix catalog data, combining two public datasets, cleaning and transforming them with Python, and visualizing insights through an interactive Power BI dashboard.

---

## 📌 Project Overview

This project simulates a real-world data engineering workflow: raw data is extracted from public sources, cleaned and merged using Python, and delivered as a business-ready dashboard. The goal is to explore what types of content Netflix offers, how its catalog has grown over time, and which titles and genres receive the highest audience ratings.

---
![Netflix Dashboard](images/dashboard_preview.png)

## 🗂️ Project Structure

```
Netflix_dashboard/
│
├── data/
│   ├── netflix_titles.csv              # Raw Netflix catalog data
│   ├── Netflix TV Shows and Movies.csv # Raw IMDB ratings data
│   └── netflix_final.csv               # Cleaned and merged dataset (pipeline output)
│
├── scripts/
│   ├── cleaning.py                      # Data cleaning, normalization and JOIN
│   └── exploration.py                   # Exploratory Data Analysis (EDA)
│
├── dashboard/
│   └── netflix_dashboard.pbix           # Power BI dashboard file
│
├── images/
│   └── dashboard_preview.png            # Dashboard screenshot
│   └── netflix.png
│
└── README.md
```

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.13 | Data cleaning and transformation |
| Pandas | Data manipulation and JOIN operations |
| Power BI Desktop | Dashboard and visualizations |
| Power Query | Additional data transformations |
| DAX | Custom measures and KPIs |
| GitHub | Version control and portfolio |

---

## ⚙️ Data Pipeline

The pipeline follows a standard ETL structure:

```
Extract          Transform              Load
──────────       ──────────────         ──────────────
netflix_titles   Clean nulls            netflix_final.csv
     +       →   Normalize types    →        ↓
titles.csv       JOIN by title            Power BI
                 + release_year
```

### Key transformation decisions

**JOIN strategy:** The two datasets were merged using a normalized title key combined with `release_year` and `type`. Titles were lowercased and stripped of punctuation before joining to maximize match rate.

**Match rate:** 3,238 out of 8,807 Netflix titles (36.8%) were successfully matched with IMDB data. The remaining titles are not present in the IMDB dataset due to differences in catalog coverage between the two sources. This is documented as a known data limitation, not a pipeline error.

**Genre normalization:** The `listed_in` column contained multiple genres per row (e.g. `"Dramas, International Movies"`). These were split into individual rows in Power Query to enable accurate genre-level analysis.

---

## 📊 Dashboard Pages

### Page 1 — Overview
High-level snapshot of the Netflix catalog. KPI cards, content distribution by type, global map and top genres.

### Page 2 — Trends
How Netflix catalog has grown over time. Line charts showing yearly growth, Movies vs TV Shows evolution, and content added by month.

### Page 3 — Content Analysis
Deep dive into catalog composition. Top 10 genres, content rating distribution (treemap), movie duration analysis (scatter plot) and top directors.

### Page 4 — IMDB Insights
Quality analysis using the enriched dataset. Top 10 rated titles, average score by genre, score vs popularity scatter plot, and an interactive decomposition tree to explore score drivers.

---

## 🔍 Key Insights

- Netflix reached its content peak in **2019** with over 2,000 titles added that year, followed by a decline in 2020-2021 likely influenced by production slowdowns.
- **Movies represent 69.6%** of the catalog, while TV Shows account for 30.4%.
- **International Movies and Dramas** are the most represented genres, reflecting Netflix's global content strategy.
- **TV-MA** is the dominant content rating, indicating that Netflix targets primarily adult audiences.
- The average IMDB score across the catalog is **6.45**, with Korean TV Shows and Classic Movies ranking among the highest-rated genres.
- A clear outlier exists in the score vs popularity scatter: one title combines a near-perfect score with over 1M votes, pointing to a globally recognized series.

---

## ▶️ How to Run

### Prerequisites
- Python 3.8+
- pandas library → `pip install pandas`
- Power BI Desktop (free)

### Steps

**1. Clone the repository**
```bash
git clone https://github.com/your-username/netflix-dashboard.git
cd netflix-dashboard
```

**2. Run the cleaning pipeline**
```bash
cd data
python ../scripts/cleaning.py
```
This generates `netflix_final.csv` in the `data/` folder.

**3. Run the EDA (optional)**
```bash
python ../scripts/exploration.py
```

**4. Open the dashboard**
Open `dashboard/netflix_dashboard.pbix` in Power BI Desktop. If prompted, update the data source path to point to your local `netflix_final.csv`.



## 👤 Author

**David Angel Carbajal Rangel**
Aspiring Data Engineer passionate about building end-to-end data pipelines and turning raw data into actionable insights.
