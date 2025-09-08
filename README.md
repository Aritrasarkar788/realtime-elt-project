# Realtime ELT Data Pipeline for Crypto Analytics

This project demonstrates how to build a "production-style, fault-tolerant realtime ELT pipeline" using "GitHub Actions, MongoDB Atlas, Kafka, PySpark, Airflow, and Docker".  
The system ingests live cryptocurrency prices, cleans and transforms them, stores them in a gold layer, and enables "BI-style analytics and forecasting".


## Project Goals
- Ingest real-time API data **continuously** (even if local PC is off).  
- Store raw → cleaned → gold data layers for reliability.  
- Perform **streaming transformations** using Kafka + PySpark.  
- Orchestrate workflows using **Airflow**.  
- Build **BI dashboards and forecasts** for business insights.  
- Design a **CV-ready, production-like system**.  


## Architecture

Components
1. Data Ingestion (GitHub Actions → MongoDB Atlas)
GitHub Actions fetches crypto prices from API every 10 minutes.
Data is stored in MongoDB Atlas as the raw layer.

2. Streaming with Kafka

mongo_to_kafka.py → reads from MongoDB Atlas → produces to raw_data_topic.
kafka_to_cleaned_kafka.py → consumes raw data → cleans → produces to cleaned_data_topic.
debug_cleaned_topic_reader.py → validation script for debugging.

3. PySpark Gold Layer

cleaned_to_gold.py consumes from cleaned_data_topic.
Parses JSON → writes structured Parquet files into:
gold_layer/crypto_prices/

5. Fault Tolerance

Runs on AZURE VM with Kafka in Docker.
supervisord keeps processes alive after restarts.
MongoDB Atlas ensures no local data loss.

## ANALYTICS
Forecasting with Prophet
Reformatted dataset (timestamp → ds, price_usd → y).
Trained Prophet with daily seasonality.
Generated 30-day price forecast with trend & seasonality components.

from prophet import Prophet

btc = pdf[["timestamp", "price_usd"]].rename(columns={"timestamp":"ds", "price_usd":"y"})

model = Prophet(daily_seasonality=True)
model.fit(btc)

future = model.make_future_dataframe(periods=30)
forecast = model.predict(future)

model.plot(forecast)

### Repository Structure
realtime-elt-project/
│── dags/                # Airflow DAGs
│── logs/                # Airflow logs
│── plugins/             # Airflow plugins
│── kafka_scripts/       # Kafka producers/consumers
│   ├── mongo_to_kafka.py
│   ├── kafka_to_cleaned_kafka.py
│   ├── debug_cleaned_topic_reader.py
│── pyspark_jobs/        # PySpark jobs
│   ├── cleaned_to_gold.py
│── gold_layer/          # Parquet files (gold data)
│── .github/workflows/   # GitHub Actions workflow (fetch_data.yml)
│── docker-compose.yml   # Docker services
│── README.md            # Project documentation



