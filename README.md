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

## Usage

### Set environment variables

- Set the redash api url and api key to environment variables

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
```

- Show query list

```bash
$ local-redash query-list
```

- Show query

```bash
$ local-redash show-query --query-id [query id]
```

- Run query

```bash
$ local-redash query --query-id [query id]
```


## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)


