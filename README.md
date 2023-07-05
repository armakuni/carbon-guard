# Carbon Guard 👮

Carbon Guard is a unique and environmentally conscious GitHub Action & CLI App
designed to help reduce the carbon footprint of your CI/CD pipelines. It
works by monitoring real-time carbon intensity data and preventing
pipelines from running when the carbon intensity is high.

## Usage

```shell,script(name="usage",expected_exit_code=0)
poetry run carbon_guard --help
```

``` ,verify(script_name="usage",stream=stdout)
                                                                                
 Usage: carbon_guard [OPTIONS]                                                  
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ *  --max-carbon-intensi…        INTEGER                Set the max carbon    │
│                                                        intensity in          │
│                                                        gCO2eq/kWh.           │
│                                                        [env var:             │
│                                                        MAX_CARBON_INTENSITY] │
│                                                        [default: None]       │
│                                                        [required]            │
│    --data-source                [file|national-grid-e  Where to read carbon  │
│                                 so-carbon-intensity|c  intensity data from   │
│                                 o2-signal]             [env var:             │
│                                                        DATA_SOURCE]          │
│                                                        [default:             │
│                                                        national-grid-eso-ca… │
│    --from-file-carbon-i…        PATH                   File to read carbon   │
│                                                        intensity from in     │
│                                                        file mode             │
│                                                        [env var:             │
│                                                        FROM_FILE_CARBON_INT… │
│                                                        [default:             │
│                                                        .carbon_intensity]    │
│    --nation-grid-eso-ca…        PARSE_URL              URL for the National  │
│                                                        Grid ESO Carbon       │
│                                                        Intensity API         │
│                                                        [env var:             │
│                                                        NATIONAL_GRID_ESO_CA… │
│                                                        [default:             │
│                                                        https://api.carbonin… │
│    --co2-signal-carbon-…        PARSE_URL              URL for the CO2       │
│                                                        Signal api            │
│                                                        [env var:             │
│                                                        CO2_SIGNAL_API_BASE_… │
│                                                        [default:             │
│                                                        https://api.co2signa… │
│    --co2-signal-api-key         TEXT                   Api key for the CO2   │
│                                                        Signal api, required  │
│                                                        in CO2 Signal mode    │
│                                                        [env var:             │
│                                                        CO2_SIGNAL_API_KEY]   │
│                                                        [default: None]       │
│    --co2-signal-country…        TEXT                   Country code to get   │
│                                                        the carbon intensity  │
│                                                        from CO2 Signal api   │
│                                                        [env var:             │
│                                                        CO2_SIGNAL_COUNTRY_C… │
│                                                        [default: None]       │
│    --help                                              Show this message and │
│                                                        exit.                 │
╰──────────────────────────────────────────────────────────────────────────────╯

```
### Common use case
When comparing current carbon intensity levels to global carbon intensity
based on gCO2eq/kWh.

Comparing carbon levels with the expected outcome for high carbon intensity:

```shell,script(name="carbon_threshold_exceeded",  expected_exit_code=1)
carbon_intensity_is 1000
poetry run carbon_guard --max-carbon-intensity=999
```

``` ,verify(script_name="carbon_threshold_exceeded", stream=stdout)
Carbon levels exceed threshold, skipping.
```

Comparing carbon levels with the expected outcome for low carbon intensity:

```shell,script(name="carbon_threshold_ok",  expected_exit_code=0)
carbon_intensity_is 999
poetry run carbon_guard --max-carbon-intensity=999
```

``` ,verify(script_name="carbon_threshold_ok", stream=stdout)
Carbon levels under threshold, proceeding.
```

## Data Sources
* [National Grid ESO Carbon Intensity](#national-grid-eso-carbon-intensity)
* [CO2 Signal](#co2-signal)

You may change the data source by specifying the `--data-source` flag.


## National Grid ESO Carbon Intensity
Using the [national-grid-eso-carbon-intensity data source](https://carbonintensity.org.uk/).
[**note**] this only supplies data for the United Kingdom.

```shell,script(name="national_grid_eso_carbon_threshold_ok",  expected_exit_code=0)
poetry run carbon_guard --data-source national-grid-eso-carbon-intensity --max-carbon-intensity=100000
```

``` ,verify(script_name="national_grid_eso_carbon_threshold_ok", stream=stdout)
Carbon levels under threshold, proceeding.
```

### CO2 Signal 
Using the [co2-signal data source](https://www.co2signal.com/)
[**note**] This data source requires an account (free/paid) which will supply an API key for usage.

```shell,script(name="co2-signal-carbon-threshold-ok",  expected_exit_code=0)
# export CO2_SIGNAL_API_KEY=<your_api_key_here>
poetry run carbon_guard --data-source co2-signal --max-carbon-intensity=100000 --co2-signal-country-code=GB
```

``` ,verify(script_name="co2-signal-carbon-threshold-ok", stream=stdout)
Carbon levels under threshold, proceeding.
```

#### Errors
if you don't provide a `co2-signal-country-code` the call will fail.
```shell,script(name="co2-signal-no-country-code-error",  expected_exit_code=1)
# export CO2_SIGNAL_API_KEY=<your_api_key_here>
poetry run carbon_guard --data-source co2-signal --max-carbon-intensity=100000
```

``` ,verify(script_name="co2-signal-no-country-code-error", stream=stdout)
No country code provided to CO2 Signal Api.
```

if you don't provide a `co2-signal-api-key` the call will fail.
```shell,script(name="co2-signal-no-api-key-error",  expected_exit_code=1)
export CO2_SIGNAL_API_KEY=""
poetry run carbon_guard --data-source co2-signal --max-carbon-intensity=100000 --co2-signal-country-code=GB
```

``` ,verify(script_name="co2-signal-no-api-key-error", stream=stdout)
No API key found for CO2 Signal API.
```

## Adding to your pipelines
This tool is intended to be run inside a pipeline to either fail or skip steps within, based on the current carbon intensity levels.

### Using GitHub Actions
If you intend to fail the build based on the carbon intensity level

```yaml,skip()
  validate-action:
    runs-on: ubuntu-latest
    steps:
      - uses: armakuni/carbon-guard@v0.4.1
        with:
          max_carbon_intensity: 500
      - run: echo Some complicated compute task
```

Alternatively if you want to simply skip a step if the carbon intensity is too high you can use the `continue-on-error` flag.

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

### Other pipelines
You can run in other pipelines as a command line tool
```shell, skip()
pip install git+https://github.com/armakuni/carbon-guard.git
carbon_guard --help
```