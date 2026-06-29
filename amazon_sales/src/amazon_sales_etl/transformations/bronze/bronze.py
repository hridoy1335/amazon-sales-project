import dlt
from pyspark.sql.functions import current_timestamp, expr

# Configuration
# These can be overridden via pipeline configuration
SOURCE_CATALOG = "dev"
SOURCE_SCHEMA = "lakehouse"
SOURCE_TABLE = "amazon"

@dlt.table(
    name="sales",
    comment="Bronze layer - Amazon sales raw data with ingestion metadata",
    table_properties={
        "quality": "bronze",
        "layer": "bronze",
        "source": "dev.lakehouse.amazon",
        "pipelines.autoOptimize.managed": "true"
    }
)
def sales():
    """
    Bronze sales table - Streams from dev.lakehouse.amazon
    Target: dev_amazon.bronze.sales
    
    Adds metadata columns:
    - ingestion_at: Timestamp when data was ingested
    - ingestion_id: Unique batch identifier
    - source_table: Source table name for lineage tracking
    """
    source_table_name = f"{SOURCE_CATALOG}.{SOURCE_SCHEMA}.{SOURCE_TABLE}"
    
    return (
        spark.readStream
             .table(source_table_name)
             .withColumns({
                 "ingestion_at": current_timestamp(),
                 "ingestion_id": expr("uuid()"),
                 "source_table": expr(f"'{source_table_name}'")
             })
    )
