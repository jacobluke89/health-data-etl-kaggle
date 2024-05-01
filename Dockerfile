# Stage 1: Python Stage
FROM python:3.11 as python-stage

ENV VENV_PATH="/app/venv"
ENV PATH="${VENV_PATH}/bin:$PATH"

# Install pipenv and set up the virtual environment
RUN pip install --upgrade pip && pip install pipenv
RUN pipenv install --deploy --ignore-pipfile

# Stage 2: Java Stage
FROM openjdk:11-jdk-slim

# Ensure `ps` command is available
RUN apt-get update && apt-get install -y procps wget
ENV JAVA_HOME=/usr/local/openjdk-11
ENV VENV_PATH="/app/.venv"
ENV PATH="${VENV_PATH}/bin:$PATH:$JAVA_HOME/bin"

# Create the /app directory
RUN mkdir -p /app

COPY . /app
WORKDIR /app

# Set ARGs for project-specific environment variables
ARG SPARK_URL
ARG SPARK_DRIVER
ARG SPARK_JAR_PATH
ARG SPARK_WAREHOUSE
ENV SPARK_URL=${SPARK_URL}
ENV SPARK_DRIVER=${SPARK_DRIVER}
ENV SPARK_JAR_PATH=${SPARK_JAR_PATH}
ENV SPARK_WAREHOUSE=${SPARK_WAREHOUSE}

# Set up Thrift Server and other necessary components
RUN wget -qO- https://archive.apache.org/dist/spark/spark-3.1.1/spark-3.1.1-bin-hadoop3.2.tgz | tar xvz -C /app && \
    ln -s /app/spark-3.1.1-bin-hadoop3.2 /app/spark

# Make scripts executable
RUN chmod +x /app/spark/sbin/start-thriftserver.sh

# Expose the Jupyter notebook port
EXPOSE 8888

# Start the Thrift Server
CMD ["/app/spark/sbin/start-thriftserver.sh", "--master", "local[*]", "--conf", "spark.sql.warehouse.dir=/opt/project/spark-warehouse", "--driver-java-options", "-Dderby.system.home=/app/spark/metastore_db"]
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]