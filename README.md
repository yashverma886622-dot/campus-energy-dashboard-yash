# Campus Energy Dashboard – Yash Verma

This is my capstone project for the course **Programming for Problem Solving using Python**.

## Objective

The goal of this project is to analyze the electricity consumption of different campus buildings and present it in a clean dashboard format. The script reads raw meter data from CSV files, cleans it, performs aggregations, generates visualizations, and creates an executive summary.

## Folder Structure

- `data/` – input CSV files (one file per building)
- `output/` – cleaned data, summary CSV, summary text file, and dashboard image
- `energy_dashboard.py` – main Python script
- `requirements.txt` – Python libraries used

## Datasets

For demonstration, I created two sample building files:

- `building_a.csv`
- `building_b.csv`

Each file contains:
- `timestamp` – date and time of the meter reading
- `kwh` – electricity consumption in kilowatt-hour

## What the Script Does

1. **Data Ingestion & Validation**
   - Reads all `.csv` files from the `data/` folder.
   - Handles missing/corrupt rows.
   - Adds metadata like building name and month.

2. **Aggregation Logic**
   - Calculates daily and weekly electricity usage.
   - Generates building-wise statistics (total, mean, min, max).

3. **Object-Oriented Design**
   - `MeterReading` class stores individual readings.
   - `Building` class stores all readings for one building and can generate its own report.
   - `BuildingManager` manages all buildings and creates building-wise summaries.

4. **Visualization Dashboard**
   - Line chart for daily consumption trend.
   - Bar chart for average weekly usage per building.
# Campus Energy Dashboard – Yash Verma

This project is my Capstone Assignment for the course **Programming for Problem Solving using Python**.  
The main idea of the project is to study the electricity consumption of different campus buildings and generate useful insights through data analysis and visualizations.

---

##  Objective

The goal of this project is to:

- Read electricity usage data from multiple CSV files.
- Clean and combine data into one dataset.
- Perform daily, weekly, and building-wise analysis.
- Use Object-Oriented Programming concepts to model the data.
- Create a combined dashboard using Matplotlib.
- Export results and generate an executive summary.

---

##  Project Folder Structure

campus-energy-dashboard-yash/
│
├── data/ # Input CSV files
│ ├── building_a.csv
│ └── building_b.csv
│
├── output/ # Auto-generated results
│ ├── cleaned_energy_data.csv
│ ├── building_summary.csv
│ ├── summary.txt
│ └── dashboard.png
│
├── energy_dashboard.py # Main Python script
├── requirements.txt # Libraries used
└── README.md # Project documentation

yaml
Copy code

---

##  Dataset Description

I created two sample datasets:

- **building_a.csv**
- **building_b.csv**

Each file contains:

| Column      | Description                                |
|-------------|--------------------------------------------|
| timestamp   | Date and time of meter reading             |
| kwh         | Electricity consumption in kilowatt-hour   |

---

##  What the Script Does

###  1. Data Ingestion & Validation
- Reads all CSV files from the `data/` folder.
- Handles errors and skips invalid rows.
- Adds building name and month automatically.

###  2. Aggregation Logic
- Calculates daily totals.
- Calculates weekly totals.
- Generates building-wise summary:
  - Total consumption  
  - Mean  
  - Min  
  - Max  

###  3. Object-Oriented Design
Classes used:
- `MeterReading`  
- `Building`  
- `BuildingManager`

These help store each reading, store readings per building, and manage all buildings.

###  4. Visualization Dashboard
Creates a single PNG with:
- Line chart (daily trend)
- Bar chart (weekly comparison)
- Scatter plot (peak-hour consumption)

Saved as **dashboard.png** in the `output/` folder.

###  5. Output Files
The script automatically generates:

- `cleaned_energy_data.csv`
- `building_summary.csv`
- `summary.txt` (executive summary)
- `dashboard.png`

---

##  How to Run the Project

1. Install the required libraries:

   ```bash
   pip install -r requirements.txt

Make sure the data/ folder contains the CSV files.

Run the script:

bash
Copy code
python energy_dashboard.py
Open the output/ folder to see:

Dashboard image

Summary text file

Cleaned data

Building summary

# Acknowledgement
This project is based on the Capstone Assignment provided in the course
Programming for Problem Solving using Python at K.R. Mangalam University.

Submitted by: Yash Verma
B.Tech CSE (AI & ML)

yaml
Copy code
