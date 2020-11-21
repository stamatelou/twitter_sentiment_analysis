from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql.functions import col, split
import re
from pyspark.sql import functions as F
from pyspark.sql.functions import udf
from textblob import TextBlob

if __name__ == "__main__":
    # create Spark session
    spark = SparkSession.builder.appName("TwitterSentimentAnalysis").getOrCreate()

    # read the tweet data from socket
    lines = spark.readStream.format("socket").option("host", "0.0.0.0").option("port", 5555).load()
    # Split the lines into words
    words = lines.select(explode(split(lines.value, "end_of_tweet")).alias("word"))
    words = words.na.replace('', None)
    words = words.na.drop()
    words = words.withColumn('word', F.regexp_replace('word', r'http\S+', ''))
    words = words.withColumn('word', F.regexp_replace('word', '@\w+', ''))
    words = words.withColumn('word', F.regexp_replace('word', '#', ''))
    words = words.withColumn('word', F.regexp_replace('word', 'RT', ''))
    words = words.withColumn('word', F.regexp_replace('word', ':', ''))

    def polarity_detection(text):
        return TextBlob(text).sentiment.polarity
    polarity_detection_udf = udf(polarity_detection, StringType())
    words =words.withColumn("polarity", polarity_detection_udf("word"))

    def subjectivity_detection(text):
        return TextBlob(text).sentiment.subjectivity
    subjectivity_detection_udf = udf(subjectivity_detection, StringType())
    words =words.withColumn("subjectivity", subjectivity_detection_udf("word"))

    words =words.repartition(1)
    #query = words.writeStream.format("parquet").option("parquet.block.size", "1KB").option("checkpointLocation", "C:/Users/20194066/PycharmProjects/gettingstarted/venv").option("path", "C:/Users/20194066/PycharmProjects/gettingstarted/venv").start()
    query = words.writeStream.queryName("all_tweets").outputMode("append").format("parquet").option("path", "C:/Users/20194066/PycharmProjects/gettingstarted/venv/parc").option("checkpointLocation", "C:/Users/20194066/PycharmProjects/gettingstarted/venv/check").trigger(processingTime='60 seconds').start()
    #query = words.writeStream.outputMode("append").format("memory").queryName("tweetquery").start()

    query.awaitTermination()

    #query = words.writeStream.format("console").outputMode("append").start()

    #data = spark.sql("select * from tweetquery").show()
'''
    import numpy as np
    import pandas as pd
    # Enable Arrow-based columnar data transfers
    spark.conf.set("spark.sql.execution.arrow.enabled", "true")
    # Create a Spark DataFrame from a pandas DataFrame using Arrow
    df = spark.sql("select * from tweetquery")

    # Convert the Spark DataFrame back to a pandas DataFrame using Arrow
    result_pdf = df.toPandas()

    print(result_pdf)
'''