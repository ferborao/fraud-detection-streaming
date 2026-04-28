from pyspark.sql import SparkSession
from pyspark.sql.types import (
    StructType, StructField,
    StringType, DoubleType, TimestampType
)
from pyspark.sql.functions import from_json, col, window, count
import redis

spark = SparkSession.builder.appName("fraud-consumer").getOrCreate()

df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:29092") \
    .option("subscribe", "transactions") \
    .load()

schema = StructType([
    StructField("transaction_id",                           StringType(), True),
    StructField("card_id",                                  StringType(), True),
    StructField("merchant_id",                              StringType(), True),
    StructField("amount",                                   DoubleType(), True),
    StructField("currency",                                 StringType(), True),
    StructField("transaction_type",                         StringType(), True),
    StructField("location",                                 StringType(), True),
    StructField("timestamp",                                TimestampType(), True)
])

# Parseo del valor del mensaje de Kafka utilizando el esquema definido
# El valor del mensaje se convierte a string y luego se parsea como JSON utilizando el esquema definido, creando una nueva columna "data" con los campos del JSON
# Luego se seleccionan los campos individuales de la columna "data" para trabajar con ellos directamente
# El resultado es un DataFrame con columnas correspondientes a los campos del JSON, como "transaction_id", "card_id", "amount", etc.
df_parsed = df.select(
    from_json(col("value").cast("string"), schema).alias("data")
).select("data.*")

# Agrupacion de transacciones por ventana de 5 minutos y card_id, contando el numero de transacciones
df_fraud = df_parsed.groupBy(
    window(col("timestamp"), "5 minutes"),
    col("card_id")
).agg(count("*").alias("tx_count")).filter(col("tx_count") > 3)

# Funcion para escribir los resultados en Redis, donde se almacena el card_id como clave y el numero de transacciones como valor
def write_to_redis(batch_df, batch_id):

    r = redis.Redis(host='redis', port=6379, db=0)
    
    for row in batch_df.collect():
        card_id = row['card_id']
        tx_count = row['tx_count']
        r.set(card_id, str(tx_count))

df_fraud.writeStream \
    .foreachBatch(write_to_redis) \
    .start() \
    .awaitTermination()