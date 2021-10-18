# dynatrace-metric-utils-python

Python utility for interacting with
the [Dynatrace v2 metrics API](https://www.dynatrace.com/support/help/dynatrace-api/environment-api/metric-v2/)
.

## Installation

To install the [latest version from PyPI](https://pypi.org/project/dynatrace-metric-utils/) run:

```shell
pip install dynatrace-metric-utils
```

## Usage

Using this library to create metric lines is a two-step process. First, create
lines using the `DynatraceMetricsFactory`. Then, serialize them using
a `DynatraceMetricsSerializer`. Furthermore, this library contains 
constants for use in projects consuming this library. This repository also
contains [an example script](example/example.py) demonstrating the use of
the `DynatraceMetricsFactory` and the `DynatraceMetricsSerializer`.

### Metric Creation

To create metrics, call one of the static methods on
the `DynatraceMetricsFactory`. Available instruments are:

- Gauge: `create_int_gauge` / `create_float_gauge`
- Counter: `create_int_counter_delta` / `create_float_counter_delta`
- Summary: `create_int_summary` / `create_float_summary`

In the simplest form, metric creation looks like this:

```python
factory = DynatraceMetricsFactory()
metric = factory.create_int_gauge("int-gauge", 23)
```

Additionally, it is possible to pass a list of dimensions to the metric upon
creation:

```python
metric_dimensions = {
    "dim1": "val1",
    "dim2": "val2",
}

metric = factory.create_int_gauge("int-gauge", 23, metric_dimensions)
```

The dimensions will be added to the serialized metric.
See [the section on dimension precedence](#dimension-precedence) for more
information.

Finally, it is also possible to add a timestamp to the metric:

```python
# Passing None for the dimensions will not add any dimensions to the metric.
# pass the timestamp as unix-time milliseconds.
metric = factory.create_int_gauge("int-gauge", 23, None, time.time() * 1000)

# Alternatively, the dimensions parameter can be skipped and timestamp can be passed as a named parameter.
metric = factory.create_int_gauge("int-gauge", 23,
                                  timestamp=time.time() * 1000)
```

If the metric timestamp is omitted or invalid, the Dynatrace server uses its 
current time upon ingestion.

### Metric serialization

The created metrics can then be serialized using
a `DynatraceMetricsSerializer`:

```python
# root level logger.
logger = logging.getLogger(__name__)
# The logger is optional. If no logger is specified, a logger will be created.
factory = DynatraceMetricsFactory(
    logger.getChild(DynatraceMetricsFactory.__name__))

# Create a list of default dimensions which are added to all metrics serialized by this serializer.
default_dims = {
    "default1": "value1",
    "default2": "value2"
}

serializer = DynatraceMetricsSerializer(
    logger.getChild(DynatraceMetricsSerializer.__name__),
    "prefix",  # metric key prefix, added to all metric names
    default_dims,  # default dimensions
    True,  # whether or not to enrich with Dynatrace metadata
    "metric-src",
    # the name of the framework that emits the metrics, e.g. 'opentelemetry'
)
metric = factory.create_int_gauge("int-gauge", 23)
print(serializer.serialize(metric))

# Should result in a line like: 
# prefix.int-gauge,default1=value1,default2=value2,dt.metrics.source=metric-src gauge,23
```

### Common constants

The constants can be accessed via the static `DynatraceMetricsApiConstants` class .

Currently available constants are:

- the default [local OneAgent metric API endpoint](https://www.dynatrace.com/support/help/how-to-use-dynatrace/metrics/metric-ingestion/ingestion-methods/local-api/) (`default_oneagent_endpoint()`)
- the limit for how many metric lines can be ingested in one
  request (`payload_lines_limit()`)

### Dynatrace Metadata enrichment

If the `enrich_with_dynatrace_metadata` toggle in
the `DynatraceMetricsSerializer`
constructor is set to `True` (=default), an attempt is made to read Dynatrace metadata. On
a host with a running OneAgent, setting this option will collect metadata and
add it as dimensions to all serialized metrics. Metadata typically consist of
the Dynatrace host ID and process group ID. More information on the underlying
feature that is used by the library can be found in
the [Dynatrace documentation](https://www.dynatrace.com/support/help/how-to-use-dynatrace/metrics/metric-ingestion/ingestion-methods/enrich-metrics/).

### Dimension precedence

Since there are multiple levels of dimensions (default, metric-specific,
serializer-specific) and duplicate keys are not allowed, there is a specified
precedence in dimension keys. Default dimensions will be overwritten by
metric-specific dimensions, and all dimensions will be overwritten by
serializer-specific dimensions if they share the same key after normalization.
Serializer-specific dimensions include
the [metadata dimensions](#dynatrace-metadata-enrichment), as well as the
metrics source, which is added as a dimension with `dt.metrics.source` as its
key if the `metrics_source` is set. Note that the serializer-specific
dimensions will only
contain [dimension keys reserved by Dynatrace](https://www.dynatrace.com/support/help/how-to-use-dynatrace/metrics/metric-ingestion/metric-ingestion-protocol/#syntax).
