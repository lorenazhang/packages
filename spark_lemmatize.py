from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from pyspark.sql.types import ArrayType, StringType
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Initialize PySpark session
spark = SparkSession.builder \
    .appName("TokenizationLemmatization") \
    .getOrCreate()

# Sample data - replace this with reading your dataset
data = [(1, "The quick brown fox jumps over the lazy dog."),
        (2, "Natural Language Processing is fun!"),
        (3, "PySpark makes processing large datasets easy.")]

# Create DataFrame
df = spark.createDataFrame(data, ["id", "text"])

# Initialize lemmatizer
lemmatizer = WordNetLemmatizer()

# Define a UDF for tokenization and lemmatization
def tokenize_and_lemmatize(text):
    # Tokenize the text
    tokens = word_tokenize(text)
    # Lemmatize each token
    lemmatized_tokens = [lemmatizer.lemmatize(token.lower()) for token in tokens]
    return lemmatized_tokens

# Register the UDF with PySpark
tokenize_and_lemmatize_udf = udf(tokenize_and_lemmatize, ArrayType(StringType()))

# Apply the UDF to the DataFrame
df = df.withColumn("tokens", tokenize_and_lemmatize_udf(df["text"]))

# Show the results
df.show(truncate=False)
