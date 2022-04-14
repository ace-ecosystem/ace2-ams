# Insert Alerts

There is a script at `bin/insert-alerts.sh` that allows you to insert alerts into the database that you then view in the GUI.

## Basic usage

To insert a single alert into the database:

```
bin/insert-alerts.sh db_api/app/tests/alerts/alert.json
```

You must pass a path to a JSON file that represents the structure of an alert's analysis and observable instance objects. There are already some example JSON files available:

```
backdb_apiend/app/tests/alerts/large.json
db_api/app/tests/alerts/small.json
```

## Adding multiple alerts

You can use the script to add multiple alerts using the same JSON file. This will add 10 separate alerts to the database:

```
bin/insert-alerts.sh db_api/app/tests/alerts/small.json 10
```

## Using a dynamic alert template

You can also use an alert template where certain tokens inside of the JSON file get replaced with dynamic/random data. An example alert template is available at `db_api/app/tests/alerts/small_template.json`.

This template uses the following tokens that get replaced with random data using Faker:

- `<ALERT_NAME>` - A random name for the alert
- `<A_TYPE>` - Three random words used for the analysis module type
- `<O_TYPE>` - A random word used for the observable type
- `<O_VALUE>` - Two random words used for the observable value
- `<TAG>` - A random word used for a tag

Using the dynamic template is the same command. To add 10 dynamic alerts to the database:

```
bin/insert-alerts.sh db_api/app/tests/alerts/small_template.json 10
```
