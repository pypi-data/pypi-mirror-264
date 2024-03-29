[![Gitter](https://img.shields.io/gitter/room/ionos-cloud/sdk-general)](https://gitter.im/ionos-cloud/sdk-general)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=sdk-python-dbaas-mariadb&metric=alert_status)](https://sonarcloud.io/summary?id=sdk-python-dbaas-mariadb)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=sdk-python-dbaas-mariadb&metric=bugs)](https://sonarcloud.io/summary/new_code?id=sdk-python-dbaas-mariadb)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=sdk-python-dbaas-mariadb&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=sdk-python-dbaas-mariadb)
[![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=sdk-python-dbaas-mariadb&metric=reliability_rating)](https://sonarcloud.io/summary/new_code?id=sdk-python-dbaas-mariadb)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=sdk-python-dbaas-mariadb&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=sdk-python-dbaas-mariadb)
[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=sdk-python-dbaas-mariadb&metric=vulnerabilities)](https://sonarcloud.io/summary/new_code?id=sdk-python-dbaas-mariadb)
[![Release](https://img.shields.io/github/v/release/ionos-cloud/sdk-python-dbaas-mariadb.svg)](https://github.com/ionos-cloud/sdk-python-dbaas-mariadb/releases/latest)
[![Release Date](https://img.shields.io/github/release-date/ionos-cloud/sdk-python-dbaas-mariadb.svg)](https://github.com/ionos-cloud/sdk-python-dbaas-mariadb/releases/latest)
[![PyPI version](https://img.shields.io/pypi/v/ionoscloud-dbaas-mariadb)](https://pypi.org/project/ionoscloud-dbaas-mariadb/)

![Alt text](.github/IONOS.CLOUD.BLU.svg?raw=true "Title")


# Python API client for ionoscloud_dbaas_mariadb

An enterprise-grade Database is provided as a Service (DBaaS) solution that
can be managed through a browser-based \"Data Center Designer\" (DCD) tool or
via an easy to use API.

The API allows you to create additional MariaDB database clusters or modify existing
ones. It is designed to allow users to leverage the same power and
flexibility found within the DCD visual tool. Both tools are consistent with
their concepts and lend well to making the experience smooth and intuitive.


## Overview
The IONOS Cloud SDK for Python provides you with access to the IONOS Cloud API. The client library supports both simple and complex requests. It is designed for developers who are building applications in Python. All API operations are performed over SSL and authenticated using your IONOS Cloud portal credentials. The API can be accessed within an instance running in IONOS Cloud or directly over the Internet from any application that can send an HTTPS request and receive an HTTPS response.


### Installation & Usage

**Requirements:**
- Python >= 3.5

### pip install

Since this package is hosted on [Pypi](https://pypi.org/) you can install it by using:

```bash
pip install ionoscloud-dbaas-mariadb
```

If the python package is hosted on a repository, you can install directly using:

```bash
pip install git+https://github.com/ionos-cloud/sdk-python-dbaas-mariadb.git
```

Note: you may need to run `pip` with root permission: `sudo pip install git+https://github.com/ionos-cloud/sdk-python-dbaas-mariadb.git`

Then import the package:

```python
import ionoscloud_dbaas_mariadb
```

### Setuptools

Install via [Setuptools](http://pypi.python.org/pypi/setuptools).

```bash
python setup.py install --user
```

or `sudo python setup.py install` to install the package for all users

Then import the package:

```python
import ionoscloud_dbaas_mariadb
```

> **_NOTE:_**  The Python SDK does not support Python 2. It only supports Python >= 3.5.

### Authentication

The username and password **or** the authentication token can be manually specified when initializing the SDK client:

```python
configuration = ionoscloud_dbaas_mariadb.Configuration(
                username='YOUR_USERNAME',
                password='YOUR_PASSWORD',
                token='YOUR_TOKEN'
                )
client = ionoscloud_dbaas_mariadb.ApiClient(configuration)
```

Environment variables can also be used. This is an example of how one would do that:

```python
import os

configuration = ionoscloud_dbaas_mariadb.Configuration(
                username=os.environ.get('IONOS_USERNAME'),
                password=os.environ.get('IONOS_PASSWORD'),
                token=os.environ.get('IONOS_TOKEN')
                )
client = ionoscloud_dbaas_mariadb.ApiClient(configuration)
```

**Warning**: Make sure to follow the Information Security Best Practices when using credentials within your code or storing them in a file.


### HTTP proxies

You can use http proxies by setting the following environment variables:
- `IONOS_HTTP_PROXY` - proxy URL
- `IONOS_HTTP_PROXY_HEADERS` - proxy headers

Each line in `IONOS_HTTP_PROXY_HEADERS` represents one header, where the header name and value is separated by a colon. Newline characters within a value need to be escaped. See this example:
```
Connection: Keep-Alive
User-Info: MyID
User-Group: my long\nheader value
```


### Changing the base URL

Base URL for the HTTP operation can be changed in the following way:

```python
import os

configuration = ionoscloud_dbaas_mariadb.Configuration(
                username=os.environ.get('IONOS_USERNAME'),
                password=os.environ.get('IONOS_PASSWORD'),
                host=os.environ.get('IONOS_API_URL'),
                server_index=None,
                )
client = ionoscloud_dbaas_mariadb.ApiClient(configuration)
```

## Certificate pinning:

You can enable certificate pinning if you want to bypass the normal certificate checking procedure,
by doing the following:

Set env variable IONOS_PINNED_CERT=<insert_sha256_public_fingerprint_here>

You can get the sha256 fingerprint most easily from the browser by inspecting the certificate.


## Documentation for API Endpoints

All URIs are relative to *https://mariadb.de-txl.ionos.com*
<details >
    <summary title="Click to toggle">API Endpoints table</summary>


| Class | Method | HTTP request | Description |
| ------------- | ------------- | ------------- | ------------- |
| BackupsApi | [**backups_find_by_id**](docs/api/BackupsApi.md#backups_find_by_id) | **GET** /backups/{backupId} | Fetch a cluster&#39;s backups |
| BackupsApi | [**backups_get**](docs/api/BackupsApi.md#backups_get) | **GET** /backups | List of cluster&#39;s backups. |
| BackupsApi | [**cluster_backups_get**](docs/api/BackupsApi.md#cluster_backups_get) | **GET** /clusters/{clusterId}/backups | List backups of cluster |
| ClustersApi | [**clusters_delete**](docs/api/ClustersApi.md#clusters_delete) | **DELETE** /clusters/{clusterId} | Delete a cluster |
| ClustersApi | [**clusters_find_by_id**](docs/api/ClustersApi.md#clusters_find_by_id) | **GET** /clusters/{clusterId} | Fetch a cluster |
| ClustersApi | [**clusters_get**](docs/api/ClustersApi.md#clusters_get) | **GET** /clusters | List clusters |
| ClustersApi | [**clusters_post**](docs/api/ClustersApi.md#clusters_post) | **POST** /clusters | Create a cluster |

</details>

## Documentation For Models

All URIs are relative to *https://mariadb.de-txl.ionos.com*
<details >
<summary title="Click to toggle">API models list</summary>

 - [Backup](docs/models/Backup)
 - [BackupList](docs/models/BackupList)
 - [BackupListAllOf](docs/models/BackupListAllOf)
 - [BackupResponse](docs/models/BackupResponse)
 - [BaseBackup](docs/models/BaseBackup)
 - [ClusterList](docs/models/ClusterList)
 - [ClusterListAllOf](docs/models/ClusterListAllOf)
 - [ClusterMetadata](docs/models/ClusterMetadata)
 - [ClusterProperties](docs/models/ClusterProperties)
 - [ClusterResponse](docs/models/ClusterResponse)
 - [ClustersGet400Response](docs/models/ClustersGet400Response)
 - [ClustersGet401Response](docs/models/ClustersGet401Response)
 - [ClustersGet403Response](docs/models/ClustersGet403Response)
 - [ClustersGet404Response](docs/models/ClustersGet404Response)
 - [ClustersGet405Response](docs/models/ClustersGet405Response)
 - [ClustersGet415Response](docs/models/ClustersGet415Response)
 - [ClustersGet422Response](docs/models/ClustersGet422Response)
 - [ClustersGet429Response](docs/models/ClustersGet429Response)
 - [ClustersGet500Response](docs/models/ClustersGet500Response)
 - [ClustersGet503Response](docs/models/ClustersGet503Response)
 - [Connection](docs/models/Connection)
 - [CreateClusterProperties](docs/models/CreateClusterProperties)
 - [CreateClusterRequest](docs/models/CreateClusterRequest)
 - [DBUser](docs/models/DBUser)
 - [DayOfTheWeek](docs/models/DayOfTheWeek)
 - [ErrorMessage](docs/models/ErrorMessage)
 - [MaintenanceWindow](docs/models/MaintenanceWindow)
 - [MariadbVersion](docs/models/MariadbVersion)
 - [Pagination](docs/models/Pagination)
 - [PaginationLinks](docs/models/PaginationLinks)
 - [State](docs/models/State)


[[Back to API list]](#documentation-for-api-endpoints) [[Back to Model list]](#documentation-for-models)

</details>