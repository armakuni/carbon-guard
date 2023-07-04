# Carbon Guard 👮

We are taking the workload to carbon guard (to carbon guard)  to carbon guard

![image](https://github.com/armakuni/carbon-guard/assets/54274482/a4791a67-ac7b-4e7a-a5e4-bf1ceb8b3a9f)


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

You can also use it as a GitHub action

```yaml,skip()
  validate-action:
    runs-on: ubuntu-latest
    steps:
      - uses: armakuni/carbon-guard@v0.4.1
        with:
          max_carbon_intensity: 500
      - run: echo Some complicated compute task
```

Alternatively if you want to simply skip if the carbon intensity is too high you can use the `continue-on-error` flag.

```yaml,skip()
  validate-action:
    runs-on: ubuntu-latest
    steps:
      - uses: armakuni/carbon-guard@v0.4.1
        continue-on-error: true
        id: carbon_guard
        with:
          max_carbon_intensity: 500
      - run: echo Some complicated compute task
        if: steps.carbon_guard.outcome == 'success'
```
