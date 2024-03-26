
# AnalyticsTool Package

## Overview

AnalyticsTool is a Python package designed to interface with PostgreSQL and MongoDB databases, utilizing AWS Secrets Manager for secure access. It provides a streamlined way to query and manipulate data, ideal for analytics and data management tasks.

## Features

- Access and manage data in PostgreSQL and MongoDB databases.
- Securely manage database credentials using AWS Secrets Manager.
- Comprehensive query functionalities to retrieve and manipulate data.

## Installation

Install AnalyticsTool via pip:

```bash
pip install web3m_analytic_tool
```

## Configuration

Before using AnalyticsTool, configure the following environment variables in your `.env` file for AWS access:

- `AWS_ACCESS_KEY`
- `AWS_SECRET_KEY`
- `REGION`

## Usage

### Initializing the Tool

Import and initialize `AnalyticsTool` with your AWS credentials:

```python
from analytics import AnalyticsTool


aws_access_key = 'your access key'
aws_secret_key = 'your secret key'
region = 'your region'

analytics = AnalyticsTool(aws_access_key, aws_secret_key, region)
```

### Example Usage

#### Fetch Data from PostgreSQL

Retrieve master user data:

```python
master_users = analytics.get_all_master_users_dict()
print(master_users)
```

#### Query Data from MongoDB

Get documents from a specific collection:

```python
documents = analytics.get_from_mongo_all_list_collection('your_collection_name')
print(documents)
```

## API Reference

### PostgreSQL Data Access

- `get_all_master_users_dict()`: Get master user data.
- `get_all_sub_users_dict()`: Get sub-user data.
- `get_all_wallet_activities_dict()`: Get wallet activity data.
- `get_all_wallets_dict()`: Get wallet data.

### MongoDB Data Access

- `get_from_mongo_all_list_collection(collection_name)`: Get all documents from a specified collection.
- `get_from_mongo_records_by_filter(collection_name, user_id=None, type=None)`: Get filtered documents from a collection.

## License

AnalyticsTool is released under the [MIT License](https://opensource.org/licenses/MIT).

## Contributing

Contributions to the AnalyticsTool project are welcome. Please refer to the `CONTRIBUTING.md` file for guidelines on how to contribute.
