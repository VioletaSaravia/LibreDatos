# Use the official Cassandra image from Docker Hub
FROM cassandra

# Set the container name and hostname
ENV CASSANDRA_NAME cassandra
ENV CASSANDRA_HOSTNAME cassandra

# Expose Cassandra ports
EXPOSE 7000 7001 7199 9042 9160

# Start Cassandra as a daemon
CMD ["cassandra", "-f"]
