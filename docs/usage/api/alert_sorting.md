# Alert Sorting

The API provides several ways to sort the alerts that are returned by the `/api/alert/` endpoint.

## Disposition

To sort the alerts by their disposition:

**Ascending**

```
/api/alert/?sort=disposition|asc
```

**Descending**

```
/api/alert/?sort=disposition|desc
```

> **NOTE:** Sorting by disposition will be skipped if you are also filtering the alerts by disposition.

## Disposition Time

To sort the alerts by their disposition time:

**Ascending**

```
/api/alert/?sort=disposition_time|asc
```

**Descending**

```
/api/alert/?sort=disposition_time|desc
```

## Disposition User

To sort the alerts by their disposition user:

**Ascending**

```
/api/alert/?sort=disposition_user|asc
```

**Descending**

```
/api/alert/?sort=disposition_user|desc
```

> **NOTE:** Sorting by disposition user will be skipped if you are also filtering the alerts by disposition user.

## Event Time

To sort the alerts by their event time:

**Ascending**

```
/api/alert/?sort=event_time|asc
```

**Descending**

```
/api/alert/?sort=event_time|desc
```

## Insert Time

To sort the alerts by their insert time:

**Ascending**

```
/api/alert/?sort=insert_time|asc
```

**Descending**

```
/api/alert/?sort=insert_time|desc
```

## Name

To sort the alerts by their name:

**Ascending**

```
/api/alert/?sort=name|asc
```

**Descending**

```
/api/alert/?sort=name|desc
```

## Owner

To sort the alerts by their owner:

**Ascending**

```
/api/alert/?sort=owner|asc
```

**Descending**

```
/api/alert/?sort=owner|desc
```

> **NOTE:** Sorting by owner will be skipped if you are also filtering the alerts by owner.

## Queue

To sort the alerts by their queue:

**Ascending**

```
/api/alert/?sort=queue|asc
```

**Descending**

```
/api/alert/?sort=queue|desc
```

> **NOTE:** Sorting by queue will be skipped if you are also filtering the alerts by queue.

## Type

To sort the alerts by their type:

**Ascending**

```
/api/alert/?sort=type|asc
```

**Descending**

```
/api/alert/?sort=type|desc
```

> **NOTE:** Sorting by type will be skipped if you are also filtering the alerts by type.
