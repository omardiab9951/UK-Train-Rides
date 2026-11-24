# UK Train Rides

A collaborative **DEPI graduation project** exploring UK train ticket transactions to understand purchase behavior, ticket pricing, route sales, and journey reliability, then extending the analysis into short-term demand forecasting and a Tableau dashboard.

> **Current status:** Exploratory Data Analysis (EDA) is complete. Data preprocessing is in progress. Forecasting and Tableau implementation are planned; database and dashboard designs are currently proposals.

---

## Table of Contents

1. [Project Idea](#project-idea)
2. [Team Members](#team-members)
3. [Work Plan](#work-plan)
4. [Roles & Responsibilities](#roles--responsibilities)
5. [KPIs](#kpis)
6. [Instructor](#instructor)
7. [Project Files](#project-files)

---

## Project Idea

The goal is to turn ticket records into clear, reproducible insights for railway operations, commercial planning, and financial analysis.

The project addresses four main questions:

- How do ticket prices, ticket classes, Railcards, and purchase channels differ?
- Which directional routes contribute the most recorded ticket-sales value?
- How do journey outcomes and refund-request rates vary?
- What ticketed-journey demand and daily sales value can be forecast for the next month?

This is an academic case study. No operational railway deployment or measured business impact is claimed.

### Dataset

The main file, `railway.csv`, contains **31,653 ticket transaction records and 18 columns**. The optional `railway_data_dictionary.csv` describes the fields; it is a reference file, not a calculation input in the final EDA notebook.

| Property | Observed value |
|---|---|
| Ticket transaction records | 31,653 |
| Columns | 18 |
| Purchase-date window | 8 December 2023–30 April 2024 |
| Journey-date window | 1 January–30 April 2024 |
| Unique transaction IDs | 31,653 |
| Duplicate full rows | 0 |

The fields cover purchase dates and times, purchase channels, payment methods, Railcards, ticket types and classes, prices, departure and arrival stations, journey dates and times, journey outcomes, disruption reasons, and refund requests.

**Record meaning matters:** each row is a ticket transaction linked to a planned journey. It is not a verified boarding, a unique passenger, or a distinct train service.

The CSV does not specify a currency. GBP is a project assumption; the analysis uses **price units** where source currency cannot be verified.

### Completed EDA

The final notebook contains **24 code cells and 10 saved chart outputs**, using pandas, NumPy, Matplotlib, and Seaborn. It separates calculations and tables from visualization cells and is organized by topic.

The completed exploration includes:

- Dataset profiling, duplicate checks, date validation, and descriptive price statistics.
- Missing-value checks and preservation of meaningful Railcard categories.
- Ticket-type, ticket-class, and Railcard comparisons.
- Purchase-channel and payment-method analysis.
- Directional route summaries and daily/monthly purchase and journey activity.
- Journey reliability, disruption reasons, refund requests, data-quality flags, and total reconciliation.

#### Selected Findings

These figures come from the final notebook's saved outputs.

| Finding | Result |
|---|---|
| Recorded ticket-sales value | **741,921 price units** |
| Mean / median ticket price | **23.44 / 11 price units** |
| Recorded price range | **1–267 price units** |
| Leading route by sales value | **London Kings Cross to York: 183,193 price units** |
| Journey-status shares | **86.82% On Time, 7.24% Delayed, 5.94% Cancelled** |
| Refund-request rates within status | **23.82% Delayed; 30.43% Cancelled** |

Overall, route, daily, and monthly purchase sales-value totals reconcile to **741,921 price units**.

Ticket-sales value is the sum of recorded prices **before refund adjustments**. It is not profit or net revenue. A refund request does not confirm that a refund was approved or paid.

#### Data-Quality Decisions

The literal Railcard value `None` means **no Railcard**, not missing information. Empty actual-arrival times for cancelled records and empty delay reasons for on-time records are retained as meaningful blanks.

Under the documented overnight-time assumption, **18 records marked Delayed** have actual arrival at or before scheduled arrival. They remain review flags rather than being automatically relabeled. High prices are also retained; an unusual value is not automatically a data error.

### Limitations

The extract-selection rule and complete purchase-date coverage are undocumented. Four months of journey history do not establish annual seasonality. Group price differences are descriptive and do not prove a causal Railcard discount effect.

The available fields do not establish unique passenger counts, verified boardings, occupancy, distinct-service capacity, actual refund payments, or operating costs. Conclusions and forecasts must remain within these boundaries.

---

## Team Members

| # | Name |
|---|---|
| 1 | George Ayman |
| 2 | Lamis Amer |
| 3 | Mohamed Waly |
| 4 | Nour El Deen |
| 5 | Omar Diab |
| 6 | Sondos Atef |

---

## Work Plan

### Project Status

| Workstream | Status | Deliverable |
|---|---|---|
| Exploratory Data Analysis | Completed | `EDA_final.ipynb` with summaries, charts, quality checks, and reconciled totals |
| Data preprocessing | In progress | Cleaned dataset, preprocessing notebook, and transformation log |
| Database implementation | Planned | Proposed schema to be implemented and validated |
| Further business analysis | Planned | Decision-relevant questions answered using SQL and Python |
| Forecasting | Planned | Next-month demand, daily sales-value forecasts, and demand by class |
| Tableau dashboard | Planned | Interactive views of analysis and evaluated forecasts |
| Final project delivery | Pending remaining implementation | Updated report, presentation, and full-project demonstration |

### Handoff Flow

Work moves in order, so each person can start when the previous stage delivers its output:

1. **Business understanding** (whole team)
2. **EDA** (Mohamed & Lamis)
3. **Preprocessing** (George & Sondos)
4. **Modeling and evaluation** (Nour)
5. **Dashboard, deployment, review, and final report** (Omar)

### Preprocessing and Forecasting Roadmap

The current preprocessing work will validate data types and chronology, document justified category standardization, preserve meaningful missing values, create useful derived fields, and export a cleaned dataset with before/after checks.

The forecasting phase must define the demand target and cancellation policy before modelling. Required outputs are:

1. The number of ticketed journeys for the month after the validated historical window.
2. Recorded ticket-sales value for each day of that month.
3. Demand by ticket class.

May 2024 is a candidate first forecasting horizon because the observed journey window ends in April 2024; coverage must be validated before using that horizon. These are forecasts of the historical case-study data, not live predictions of current UK rail traffic.

Models will be compared with simple baselines using chronological evaluation. Learned preprocessing must use training data only. No model accuracy, forecast values, or deployed dashboard are reported at this stage.

### Tools and Technologies

| Tool | Use | Stage |
|---|---|---|
| Python, pandas, NumPy | Data inspection, aggregation, and preprocessing | EDA complete; preprocessing in progress |
| Matplotlib, Seaborn | Statistical charts and visual exploration | Used in EDA |
| Jupyter | Reproducible analysis notebooks | Used in EDA |
| SQL | Analytical data model and business queries | Planned implementation |
| PostgreSQL | Proposed database-design target | Draft design only |
| scikit-learn | Candidate forecasting and evaluation workflows | Planned |
| Tableau | Interactive analytical dashboard | Proposed design; implementation planned |

---

## Roles & Responsibilities

| Team member | Role | Responsibilities |
|---|---|---|
| **George Ayman** | Data & Preprocessing | Handle duplicates, feature selection, and missing values |
| **Lamis Amer** | Data & EDA | Statistics, visualizations, EDA report, and ERD (shared with Mohamed) |
| **Mohamed Waly** | Data & EDA | Statistics, visualizations, EDA report, and ERD (shared with Lamis) |
| **Nour El Deen** | ML Lead | Modeling and evaluation, including the forecasting workflow |
| **Omar Diab** | Dashboard Lead | Tableau dashboard, deployment (live dashboards), project review, and final report |
| **Sondos Atef** | Data & Preprocessing | Handle outliers and skewness, feature engineering, and scaling |

All members take part in the business-understanding phase.

---

## KPIs

> The KPIs below are proposed from the project's questions and workstreams. Confirm them with the team and instructor.

### Business and Analysis KPIs

These are the metrics the project reports on. Current values come from the completed EDA.

| KPI | Current value |
|---|---|
| Recorded ticket-sales value (before refunds) | 741,921 price units |
| Mean / median ticket price | 23.44 / 11 price units |
| Journey-status shares (On Time / Delayed / Cancelled) | 86.82% / 7.24% / 5.94% |
| Refund-request rate within status (Delayed / Cancelled) | 23.82% / 30.43% |
| Top route by sales value | London Kings Cross to York (183,193 price units) |

### Forecasting KPIs

- Next-month ticketed-journey demand, forecast and compared with simple baselines.
- Daily ticket-sales value for the forecast month.
- Demand by ticket class.
- Forecast error measured with chronological evaluation. No accuracy has been reported yet.

### Delivery KPIs

- Each workstream in the Project Status table reaches "Completed".
- Cleaned dataset delivered, with a before/after transformation log.
- Dashboard delivered with the analysis and the evaluated forecasts.
- Final report and presentation updated after implementation.

---

## Instructor

**Islam Atef**

---


## Project Files

All the required project files (documents, EDA notebook, dataset, and the files of every phase) are available in this Google Drive folder:

🔗 [UK Train Rides - Project Drive](https://drive.google.com/drive/folders/16Se_FEQ1GIvIaQPHEHbhDzrtH3sJj-8S?usp=sharing)

### Getting Started

#### 1. Obtain the project files

Clone the repository:

```bash
git clone https://github.com/omardiab9951/UK-Train-Rides.git
cd UK-Train-Rides
```

Ensure the following files exist locally:

- `System/EDA_Phase/EDA_final.ipynb`
- `Dataset/railway.csv`

The source CSV is required to execute the notebook. Its availability and redistribution permissions must be confirmed; do not assume it is included merely because the repository is public.

#### 2. Create a Python environment

Python 3.10 or newer is recommended. From the repository root:

```bash
python -m venv .venv
```

Activate it on macOS/Linux:

```bash
source .venv/bin/activate
```

Or in Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

If your system uses `python3` rather than `python`, use that command when creating the environment.

#### 3. Install the EDA dependencies

```bash
python -m pip install numpy pandas matplotlib "seaborn>=0.12" jupyterlab
```

Seaborn 0.12 or newer is needed for the plotting API used in the notebook. These instructions are a dependency guide, not a frozen environment lockfile.

#### 4. Run the notebook

Launch JupyterLab from the notebook directory:

```bash
cd System/EDA_Phase
jupyter lab
```

Open `EDA_final.ipynb`, select the correct Python environment, restart the kernel, and run all cells in order.

The notebook reads `../../Dataset/railway.csv`. Its working directory must therefore be `System/EDA_Phase`, including when it is opened through another notebook editor.

### Attribution and Licensing

This repository is maintained by the UK Train Rides DEPI project team. Add the verified dataset source and applicable dataset license before redistributing the CSV. A code license should be selected explicitly; no dataset permission or open-source license is assumed by this README.
