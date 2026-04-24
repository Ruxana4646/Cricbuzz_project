#  Cricbuzz Analytics Dashboard

A **real-time cricket analytics platform** built using a complete **ETL (Extract, Transform, Load) data pipeline**.  
This project fetches live cricket data from the Cricbuzz API, processes it, stores it in MySQL, and visualizes insights using Streamlit.

---

#  Features

- Live match tracking (Cricbuzz-style UI)
- Player performance analytics dashboard
- CRUD operations for player data
- SQL-based insights and aggregations
- Professional dark blue themed UI
- End-to-end data pipeline execution

---

#  Tech Stack

| Technology | Purpose |
|-----------|--------|
| Python | Core programming |
| MySQL | Database |
| Streamlit | Dashboard UI |
| Pandas | Data processing |
| Requests | API integration |

---

#  Data Pipeline (ETL)

Cricbuzz API
↓
Extract (Python - requests)
↓
Transform (data cleaning & formatting)
↓
Load (MySQL database)
↓
Analyze (SQL queries)
↓
Visualize (Streamlit dashboard)


---

#  Project Structure
Circbuzz project/
│
├── app.py # Main Streamlit application
├── db_connection.py # MySQL connection setup
├── extract.py # Data extraction logic
├── insert.py # Data loading logic
│
├── pages/
│ ├── Live_Matches.py # Live matches UI (cards + filters)
│ ├── Player_Stats.py # Analytics dashboard
│ └── CRUD.py # CRUD operations (Add/Update/Delete)

