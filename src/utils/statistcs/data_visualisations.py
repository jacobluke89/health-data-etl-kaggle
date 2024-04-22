from pyspark.sql import DataFrame
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


def plot_age_distribution_with_sd(df: DataFrame, avg_age: float = 40.2):
    """
    This data visualisation plots the age distribution and shows 1sd either side of the avg average age.
    where the default age is defined as the UK, obtained from the Office of National Statistical.
    Args:
        df (DataFrame): The DataFrame of containing the aggregated ages and population totals.
        avg_age:  The average age of the population, defined as 40.2 default age, UK.
    """
    if "Age" in df.columns and "count" in df.columns:
        renamed_df = (df.withColumnRenamed("Age", "age")
                      .withColumnRenamed("count", "population_total")
                      )
        pandas_df = renamed_df.toPandas()
    else:
        pandas_df = df.toPandas()

    mean_age = avg_age

    pandas_df['age'] = pandas_df['age'].astype(float)
    pandas_df['population_total'] = pandas_df['population_total'].astype(int)
    pandas_df['weighted_squared_diff'] = pandas_df['population_total'] * (pandas_df['age'] - mean_age) ** 2

    total_weighted_squared_diff = np.sum(pandas_df['weighted_squared_diff'])
    total_population = np.sum(pandas_df['population_total'])

    weighted_variance = total_weighted_squared_diff / total_population
    standard_deviation = np.sqrt(weighted_variance)

    plt.figure(figsize=(12, 6))
    sns.histplot(pandas_df, x='age', weights='population_total',
                 bins=range(int(pandas_df['age'].min()), int(pandas_df['age'].max()) + 1), color='skyblue', kde=False)

    plt.axvline(mean_age, color='red', linestyle='dashed', linewidth=1)
    plt.axvline(mean_age + standard_deviation, color='green', linestyle='dashed', linewidth=1)
    plt.axvline(mean_age - standard_deviation, color='green', linestyle='dashed', linewidth=1)

    plt.axvspan(float(mean_age) - standard_deviation, float(mean_age) + standard_deviation, alpha=0.1, color='green')

    plt.title('Age Distribution with Standard Deviation')
    plt.xlabel('Age')
    plt.ylabel('Population Total')
    plt.show()


def plot_kernel_density_age_distribution(df: DataFrame):
    """
    This function plots the kernel density age distribution
    Args:
        df:

    Returns:

    """
    if "Age" in df.columns and "count" in df.columns:
        renamed_df = (df.withColumnRenamed("Age", "age")
                      .withColumnRenamed("count", "population_total")
                      )
        pandas_df = renamed_df.toPandas()
    else:
        pandas_df = df.toPandas()

    # Set the size of the plot
    plt.figure(figsize=(12, 6))

    # Create the KDE plot
    sns.kdeplot(data=pandas_df, x='age', weights='population_total', fill=True, common_norm=False, bw_adjust=0.5,
                clip=(pandas_df['age'].min(), pandas_df['age'].max()))

    plt.axvline(x=40.2, color='r', linestyle='--')

    plt.title('Kernel Density Estimate of Age Distribution')
    plt.xlabel('Age')
    plt.ylabel('Density')

    plt.show()
