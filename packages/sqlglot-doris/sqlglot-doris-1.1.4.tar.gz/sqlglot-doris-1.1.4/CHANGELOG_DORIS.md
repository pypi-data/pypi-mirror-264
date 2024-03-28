Changelog
=========

## [v1.0.2] - 2024-03-19
### :sparkles: New Features
- [`2237660`](https://github.com/selectdb/sqlglot/commit/2237660addde4be8353df0d7453c1b24a827f52b) - Automatic conversion of create table statements is supported, including
  - mysql
  - hive
  - presto
  - clickhouse

## [v1.0.1] - 2024-02-18
### :sparkles: New Features
- [`4a8eb691`](https://github.com/selectdb/sqlglot/commit/4a8eb691961e624a7b5d569b2bd8a67386235788) - support explain verbose,explain memo plan,explain physical plan,explain shape plan
  - Automatic conversion of explain statements is supported, including
    - explain
    - explain verbose
    - explain mem plan
    - explain physical plan
    - explain shape plan
- [`10b4e690`](https://github.com/selectdb/sqlglot/commit/10b4e6900913ec4b08b80ebbd254a4b054cb4976) - support match_any/match_all parse
### :bug: Bug Fixes
- Fixed format conversion conflicts in the date function 
- Improved the json type function path parsing and conversion function 
- Repaired several conversion error cases in actual scenarios, optimized the analytic generation of multiple cases, and improved the compatibility to a greater extent