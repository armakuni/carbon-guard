# Carbon Guard 👮

We are taking the workload to carbon guard (to carbon guard)  to carbon guard


## Usage

```shell,script(name="usage", expected_exit_code=0)
poetry run carbon_guard --help
```

``` ,verify(script_name="usage", stream=stdout)
                                                                                
 Usage: carbon_guard [OPTIONS]                                                  
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ *  --max-carbon-intensi…        INTEGER               Set the max carbon     │
│                                                       intensity in           │
│                                                       gCO2eq/kWh.            │
│                                                       [env var:              │
│                                                       MAX_CARBON_INTENSITY]  │
│                                                       [default: None]        │
│                                                       [required]             │
│    --data-source                [file|uk-carbon-inte  Where to read carbon   │
│                                 nsity]                intensity data from    │
│                                                       [env var:              │
│                                                       REPOSITORY_MODE]       │
│                                                       [default:              │
│                                                       uk-carbon-intensity]   │
│    --from-file-carbon-i…        PATH                  File to read carbon    │
│                                                       intensity from in file │
│                                                       mode                   │
│                                                       [env var:              │
│                                                       FROM_FILE_CARBON_INTE… │
│                                                       [default:              │
│                                                       .carbon_intensity]     │
│    --uk-carbon-intensit…        PARSE_URL             URL for the carbon     │
│                                                       intensity API          │
│                                                       [env var:              │
│                                                       UK_CARBON_INTENSITY_A… │
│                                                       [default:              │
│                                                       https://api.carbonint… │
│    --help                                             Show this message and  │
│                                                       exit.                  │
╰──────────────────────────────────────────────────────────────────────────────╯

```
### Examples
Examples for comparing current carbon intensity levels to global carbon intensity
based on gCO2eq/kWh.

Comparing carbon levels with the expected outcome for high carbon intensity:
```shell,script(name="carbon_check",  expected_exit_code=1)
carbon_intensity_is 1000
poetry run carbon_guard --max-carbon-intensity=999
```

``` ,verify(script_name="carbon_check", stream=stdout)
Carbon levels exceed threshold, skipping.
```

Comparing carbon levels with the expected outcome for low carbon intensity:
```shell,script(name="carbon_check",  expected_exit_code=0)
carbon_intensity_is 999
poetry run carbon_guard --max-carbon-intensity=999
```

``` ,verify(script_name="carbon_check", stream=stdout)
Carbon levels under threshold, proceeding.
```


You may change the data source by specifying the `--data-source` flag.

```shell,script(name="carbon_check",  expected_exit_code=0)
poetry run carbon_guard --data-source uk-carbon-intensity --max-carbon-intensity=100000
```

``` ,verify(script_name="carbon_check", stream=stdout)
Carbon levels under threshold, proceeding.
```