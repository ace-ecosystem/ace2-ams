# Alert Filters

The API provides several ways to query for and filter alerts. Any of the filters can be combined with one another to produce complex queries.

> **NOTE:** If you combine multiple filters or use one of the filters that allows you to specify a comma-separated list of items, they are all queried for using `AND` logic.

## Disposition

To fetch all alerts that were assigned a disposition of `DELIVERY`:

```
/api/alert/?disposition=DELIVERY
```

To fetch all alerts that have not yet been dispositioned:

```
/api/alert/?disposition=none
```

## Disposition User

To fetch all alerts that were dispositioned by the username `bob`:

```
/api/alert/?disposition_user=bob
```

## Dispositioned After

To fetch all alerts that were dispositioned after January 1, 2021:

```
/api/alert/?dispositioned_after=2021-01-01+00:00:00.000000+00:00
```

> **NOTE:** All timestamps are stored in the database using UTC.
>
> You will also need to ensure that the timestamp that you pass in is properly url-encoded.

## Dispositioned Before

To fetch all alerts that were dispositioned before January 1, 2021:

```
/api/alert/?dispositioned_before=2021-01-01+00:00:00.000000+00:00
```

> **NOTE:** All timestamps are stored in the database using UTC.
>
> You will also need to ensure that the timestamp that you pass in is properly url-encoded.

## Event UUID

To fetch all alerts that are associated with the event UUID `98dab2bf-2683-48e7-8193-183c3c5e4490`:

```
/api/alert/?event_uuid=98dab2bf-2683-48e7-8193-183c3c5e4490
```

## Event Time After

To fetch all alerts with the event_time after January 1, 2021:

```
/api/alert/?event_time_after=2021-01-01+00:00:00.000000+00:00
```

> **NOTE:** All timestamps are stored in the database using UTC.
>
> You will also need to ensure that the timestamp that you pass in is properly url-encoded.

## Event Time Before

To fetch all alerts that were event_time before January 1, 2021:

```
/api/alert/?event_time_before=2021-01-01+00:00:00.000000+00:00
```

> **NOTE:** All timestamps are stored in the database using UTC.
>
> You will also need to ensure that the timestamp that you pass in is properly url-encoded.

## Insert Time After

To fetch all alerts with the insert_time after January 1, 2021:

```
/api/alert/?insert_time_after=2021-01-01+00:00:00.000000+00:00
```

> **NOTE:** All timestamps are stored in the database using UTC.
>
> You will also need to ensure that the timestamp that you pass in is properly url-encoded.

## Insert Time Before

To fetch all alerts that were insert_time before January 1, 2021:

```
/api/alert/?insert_time_before=2021-01-01+00:00:00.000000+00:00
```

> **NOTE:** All timestamps are stored in the database using UTC.
>
> You will also need to ensure that the timestamp that you pass in is properly url-encoded.

## Name

To fetch all alerts with `asdf` in their name:

```
/api/alert/?name=asdf
```

> **NOTE:** This performs a substring match.

## Observable

To fetch all alerts that contain a specific observable with the type of `fqdn` and value of `google.com`:

```
/api/alert/?observable=fqdn|google.com
```

## Observable Types

To fetch all alerts that contain observables with the types of `fqdn` and `ip`:

```
/api/alert/?observable_types=fqdn,ip
```

## Observable Value

To fetch all alerts that contain observables (regardless of their type) that have the value `google.com`:

```
/api/alert/?observable_value=google.com
```

## Owner

To fetch all alerts that are owned by the username `bob`:

```
/api/alert/?owner=bob
```

## Queue

To fetch all alerts that are inside of the alert queue `intel`:

```
/api/alert/?queue=intel
```

## Tags

To fetch all alerts that have the tags `email` and `malicious`:

```
/api/alert/?tags=email,malicious
```

## Threat Actor

To fetch all alerts that were assigned the threat actor `Bad Guy`:

```
/api/alert/?threat_actor=Bad Guy
```

## Threats

To fetch all alerts that were assigned the threats `emotet` and `zbot`:

```
/api/alert/?threats=emotet,zbot
```

## Tool

To fetch all alerts produced by the tool `Splunk`:

```
/api/alert/?tool=Splunk
```

## Tool Instance

To fetch all alerts produced by the tool instance `splunkserver1`:

```
/api/alert/?tool_instance=splunkserver1
```

## Type

To fetch all alerts of type `SMTP`:

```
/api/alert/?type=SMTP
```

## Combining timestamp filters

You can combine the various timestamp filters to get alerts from a single day. For example, to get alerts that were dispositioned during November 1, 2021:

```
/api/alert/?dispositioned_after=2021-11-01+00:00:00.000000+00:00&dispositioned_before=2021-11-02+00:00:00.000000+00:00
```

> **NOTE:** All timestamps are stored in the database using UTC.
>
> You will also need to ensure that the timestamp that you pass in is properly url-encoded.
