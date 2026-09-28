# PyBroker

PyBroker is a lightweight message broker built from scratch in Python.

The project is designed to explore the internals of messaging systems such
as RabbitMQ and Kafka without relying on an existing message queue.

## Goals

PyBroker will progressively implement:

- TCP client/server communication
- Producers and consumers
- Named queues
- Publish/subscribe messaging
- Multiple concurrent clients
- ACK/NACK
- Message persistence
- Retries
- Dead-letter queues
- Consumer groups
- Heartbeats
- Management API
- Metrics
- Docker deployment
- CI testing

## Architecture

```text
Producer
   |
   v
+-------------+
|   Broker    |
+-------------+
   |
   v
+-------------+
|    Queue    |
+-------------+
   |
   v
Consumer