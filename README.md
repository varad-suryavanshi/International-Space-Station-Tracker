# 🚀 International Space Station (ISS) Tracker

This project tracks the International Space Station (ISS) in **real-time** using a big data pipeline and visualizes its geospatial coordinates using **Apache Kafka**, **Apache Spark**, and **Power BI Desktop**.

---

## 📌 Overview

- 🌐 **Live Data Source**: [open-notify API](http://api.open-notify.org/iss-now.json)
- 🧵 **Streaming Framework**: Apache Kafka
- ⚡ **Real-Time Processing**: Apache Spark Structured Streaming
- 📊 **Dashboarding**: Power BI Desktop

---

## 🛠️ Tech Stack

| Layer        | Tool/Tech                  |
|--------------|----------------------------|
| Data Source  | open-notify API            |
| Producer     | Python + Kafka Producer    |
| Messaging    | Apache Kafka               |
| Processing   | Apache Spark (Structured)  |
| Storage      | Parquet (converted to CSV) |
| Visualization| Power BI Desktop (Windows) |

---

## 📂 Project Structure

```
iss-tracker-kafka-spark-powerbi/
├── kafka_producer/
│   └── producer.py
├── spark_streamer/
│   └── spark_stream.py
├── data/
│   ├── iss_parquet/     ← Spark output (Parquet)
│   └── iss_csv/         ← Flattened CSVs for Power BI
├── requirements.txt
├── .gitignore
└── README.md
```

---

## ⚙️ How It Works

1. **Producer**: Fetches live ISS position data every 5 seconds and sends it to a Kafka topic.
2. **Spark Streaming**: Reads from Kafka, parses JSON, and writes data to Parquet files.
3. **Data Conversion**: Parquet is converted to CSV using Spark.
4. **Power BI**: Loads the CSV and creates visuals like maps and time series.

---

## ▶️ Getting Started

### 1. **Install Requirements**

- Apache Kafka & Zookeeper
- Apache Spark (3.x)
- Power BI Desktop
- Python 3.x (with `kafka-python`, `requests`, `pyspark`)

```bash
pip install -r requirements.txt
```

---

### 2. **Start Kafka and Create Topic**

```bash
# Start Zookeeper
bin/zookeeper-server-start.sh config/zookeeper.properties

# Start Kafka
bin/kafka-server-start.sh config/server.properties

# Create Kafka topic
bin/kafka-topics.sh --create --topic iss-location --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
```

---

### 3. **Run Spark Streaming App**

```bash
spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0 spark_streamer/spark_stream.py
```

---

### 4. **Run Kafka Producer**

```bash
python kafka_producer/producer.py
```

---

### 5. **Convert Parquet to CSV (in spark-shell)**

```scala
val df = spark.read.parquet("data/iss_parquet/")
val flatDf = df.select($"message", $"timestamp", $"iss_position.latitude".alias("latitude"), $"iss_position.longitude".alias("longitude"))
flatDf.write.option("header", "true").mode("overwrite").csv("data/iss_csv/")
```

---

## 📊 Power BI Dashboard (Windows)

### Steps:

1. Open **Power BI Desktop**
2. Click **Get Data → Folder** and select `data/iss_csv/`
3. Combine the CSV files
4. Transform:
   - Expand columns
   - Convert `timestamp` using:
     ```powerquery
     = #datetime(1970, 1, 1, 0, 0, 0) + #duration(0, 0, 0, [timestamp])
     ```
5. Create visuals:
   - Map (Latitude, Longitude)
   - Line chart (ISS path over time)

---

## 📦 Author

**Varad Suryavanshi**  
📧 varad.suryavanshi@example.com  
🔗 [LinkedIn](https://www.linkedin.com/in/varad-suryavanshi-a1b975227/) • [GitHub](https://github.com/varad-suryavanshi)

---

## ⭐️ Star This Repo

If you found this project useful, consider starring ⭐ the repo to show your support!
