# Local Redash

local-redash is a command line client for redash.

## Description

local-redash is a command line tool that can list queries, list data sources, execute queries and display results.

## Supported Python Versions

3.10.x and greater

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install local-redash.

```bash
pip install local-redash
```

## Configuration

The configuration file is automatically created in `~/.config/local_redash/config.yml` at first startup. See the file itself for a description of all available options.
The data is displayed using [python-tabulate](https://github.com/astanin/python-tabulate), which can be configured in the `table_format` of the config.yml.

## Usage

### Set environment variables

- Set the redash api url and api key to environment variables
  - **REDASH_URL**: Sets the API endpoint, which will be the base URL for Redash.
  - **API_KEY**: Set the redash API key.You can find it on the User Profiles page.
- Check the [redash](https://redash.io/help/user-guide/integrations-and-api/api) documentation for details.

```bash
$ export REDASH_URL=YOUR_REDASH_API_URL
$ export API_KEY=YOUR_REDASH_API_KEY
```

### CLI Usage

- Show help
```bash
$ local-redash --help

Usage: local-redash [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  data-source-list
  export-query
  query
  query-list
  show-query
```

- Show data source list

```bash
$ local-redash data-source-list

+------+--------+----------------+----------+----------+-------------+--------+
|   id | name   | pause_reason   | syntax   |   paused | view_only   | type   |
+======+========+================+==========+==========+=============+========+
|    1 | test   | None           | sql      |        0 | False       | pg     |
+------+--------+----------------+----------+----------+-------------+--------+
```

- Show query list
  - Columns to be displayed are set in config.yml.

```bash
$ local-redash query-list

+------+-------------------------+------------------+-----------------------+--------------------------+--------------------------+
|   id | name                    |   data_source_id | runtime               | retrieved_at             | created_at               |
+======+=========================+==================+=======================+==========================+==========================+
|    1 | test-01                 |                1 | 0.0031499862670898438 | 2023-01-01T00:00:00.000Z | 2023-01-01T00:00:00.000Z |
+------+-------------------------+------------------+-----------------------+--------------------------+--------------------------+
|    2 | test-02                 |                1 | 0.0031499862670898438 | 2023-01-01T00:00:00.000Z | 2023-01-01T00:00:00.000Z |
+------+-------------------------+------------------+-----------------------+--------------------------+--------------------------+
|    3 | test-03                 |                1 | 18.041463136672974    | 2023-01-01T00:00:00.000Z | 2023-01-01T00:00:00.000Z |
+------+-------------------------+------------------+-----------------------+--------------------------+--------------------------+
```

- Show query

```bash
$ local-redash show-query --query-id [query id]

+----------------------------------------------------------------------------------------------------------------------+
| query                                                                                                                |
+======================================================================================================================+
| select     film.film_id,     film.title,     film,     description,     rating from film inner join film_category on |
| film.film_id = film_category.film_id inner join category on film_category.category_id = category.category_id where   |
| category.name = 'Comedy'                                                                                             |
+----------------------------------------------------------------------------------------------------------------------+
```

- Run query

```bash
$ local-redash query --query-file [query file path] --data-source-id [data source]

ex. $ local-redash query --query-file ./select_test.sql --data-source-id 1

+---------------+----------+----------------------+
|   language_id | name     | last_update          |
+===============+==========+======================+
|             1 | English  | 2022-02-15T10:02:19Z |
+---------------+----------+----------------------+
|             2 | Italian  | 2022-02-15T10:02:19Z |
+---------------+----------+----------------------+
|             3 | Japanese | 2022-02-15T10:02:19Z |
+---------------+----------+----------------------+
|             4 | Mandarin | 2022-02-15T10:02:19Z |
+---------------+----------+----------------------+
|             5 | French   | 2022-02-15T10:02:19Z |
+---------------+----------+----------------------+
|             6 | German   | 2022-02-15T10:02:19Z |
+---------------+----------+----------------------+
```

- Export query

```bash
$ local-redash export-query --query-name [query name] ----file-path [file path]

ex. $ local-redash export-query --query-name "query_test" --file-path ./

+------------------------+
| exported-query         |
+========================+
| select * from language |
+------------------------+
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)


