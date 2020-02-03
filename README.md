# nwpc-workflow-log-model

A database model for workflow log in NWPC.

## Introduction

Model classes for MongoDB and relational database.

## MongoDB

Use MongoDB to store analytics results including node tree and node status.

- `blob`: Base class for all MongoDB documents.
- `NodeTreeBlob`: blob for node tree.
- `NodeStatusBlob`: blob for node status.

## relational database

- `owner`: Owner table
- `repo`: Repo table
- `SmsRepo`: Repo for SMS
- `EcflowRepo`: Repo for ecFlow
- `RepoVersion`: Repo versions
- `RecordBase`: base class for Records
- `SmsRecord`: SMS records
- `EcflowRecord`: ecFlow records

## Tool

use `creat_tables.py` to create all tables for NWPC Operation Systems in MySQL.

## LICENSE

Copyright &copy; 2018-2020, perillaroc at nwpc-oper.

`nwpc-workflow-log-model` is licensed under [GPL v3.0](LICENSE.md)