# Snowflake Load Pattern & DAG Orchestration

## Overview
I'm mostly familiar with Databricks; however, I wanted to try out building common ETL patterns in Snowflake as a learning experience. This folder contains examples of Snowflake notebooks demonstrating ETL workflows and DAG orchestration.

## Notebooks

### `snowflake_load_pattern_example.ipynb`
Demonstrates a common ETL pattern in Snowflake, including data loading, transformation, and pipeline workflows.

### `DAG_ORCHESTRATOR.ipynb`
A simple instructional notebook showing how to create and manage task dependencies using Snowflake's DAG (Directed Acyclic Graph) library. This example demonstrates:
- Setting up task dependencies between notebooks
- Deploying DAGs programmatically
- Testing and monitoring task execution

## Prerequisites
- Snowflake account with notebook support
- Access to a warehouse (e.g., `COMPUTE_WH`)
- Database and schema permissions for creating tasks and DAGs

## Notes
- These notebooks are designed to run in the Snowflake notebook environment
- Replace database names, schema names, and warehouse names with your own values
- The DAG example uses placeholder notebook names (`TASK_A`, `TASK_B`) that should be replaced with actual notebook names