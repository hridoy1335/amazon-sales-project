# Databricks notebook source
# MAGIC %md
# MAGIC # Amazon Sales Data Ingestion

# COMMAND ----------

dbutils.widgets.text("catalog", "main")
dbutils.widgets.text("schema", "amazon_sales")
dbutils.widgets.text("env", "dev")

catalog = dbutils.widgets.get("catalog")
schema = dbutils.widgets.get("schema")
env = dbutils.widgets.get("env")

print(f"Environment: {env}")
print(f"Target: {catalog}.{schema}")

