# Carbon Guard 👮

Carbon Guard is a unique and environmentally conscious GitHub Action & CLI App
designed to help reduce the carbon footprint of your CI/CD pipelines. It
works by monitoring real-time carbon intensity data and preventing
pipelines from running when the carbon intensity is high.

## Usage


```shell,script(name="usage",expected_exit_code=0)
uv run carbon_guard --help
```

``` ,verify(script_name="usage",stream=stdout)
                                                                                
 Usage: carbon_guard [OPTIONS] COMMAND [ARGS]...                                
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --install-completion          Install completion for the current shell.      │
│ --show-completion             Show completion for the current shell, to copy │
│                               it or customize the installation.              │
│ --help                        Show this message and exit.                    │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────╮
│ check      Check the current carbon intensity.                               │
│ schedule   Find the lowest carbon time.                                      │
╰──────────────────────────────────────────────────────────────────────────────╯

```

### Check

```shell,script(name="usage-check",expected_exit_code=0)
uv run carbon_guard check --help
```

``` ,verify(script_name="usage-check",stream=stdout)
                                                                                
 Usage: carbon_guard check [OPTIONS]                                            
                                                                                
 Check the current carbon intensity.                                            
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ *  --max-carbon-in…                       INTEGER           Set the max      │
│                                                             carbon intensity │
│                                                             in gCO2eq/kWh.   │
│                                                             [env var:        │
│                                                             MAX_CARBON_INTE… │
│                                                             [default: None]  │
│                                                             [required]       │
│    --advise-only       --no-advise-on…                      Do not exit with │
│                                                             an error if the  │
│                                                             carbon intensity │
│                                                             is above the max │
│                                                             carbon           │
│                                                             intensity.       │
│                                                             [env var:        │
│                                                             ADVISE_ONLY]     │
│                                                             [default:        │
│                                                             no-advise-only]  │
│    --data-source                          [file|national-g  Where to read    │
│                                           rid-eso-carbon-i  carbon intensity │
│                                           ntensity|co2-sig  data from        │
│                                           nal]              [env var:        │
│                                                             DATA_SOURCE]     │
│                                                             [default:        │
│                                                             national-grid-e… │
│    --from-file-car…                       PATH              File to read     │
│                                                             carbon intensity │
│                                                             from in file     │
│                                                             mode             │
│                                                             [env var:        │
│                                                             FROM_FILE_CARBO… │
│                                                             [default:        │
│                                                             .carbon_intensi… │
│    --national-grid…                       HTTP_OR_HTTPS_UR  URL for the      │
│                                           L                 National Grid    │
│                                                             ESO Carbon       │
│                                                             Intensity API    │
│                                                             [env var:        │
│                                                             NATIONAL_GRID_E… │
│                                                             [default:        │
│                                                             https://api.car… │
│    --co2-signal-ca…                       HTTP_OR_HTTPS_UR  URL for the CO2  │
│                                           L                 Signal api       │
│                                                             [env var:        │
│                                                             CO2_SIGNAL_API_… │
│                                                             [default:        │
│                                                             https://api.co2… │
│    --co2-signal-ap…                       TEXT              Api key for the  │
│                                                             CO2 Signal api,  │
│                                                             required in CO2  │
│                                                             Signal mode      │
│                                                             [env var:        │
│                                                             CO2_SIGNAL_API_… │
│                                                             [default: None]  │
│    --co2-signal-co…                       TEXT              Country code to  │
│                                                             get the carbon   │
│                                                             intensity from   │
│                                                             CO2 Signal api   │
│                                                             [env var:        │
│                                                             CO2_SIGNAL_COUN… │
│                                                             [default: None]  │
│    --help                                                   Show this        │
│                                                             message and      │
│                                                             exit.            │
╰──────────────────────────────────────────────────────────────────────────────╯

```

### Schedule

```shell,script(name="usage-schedule",expected_exit_code=0)
uv run carbon_guard schedule --help
```

``` ,verify(script_name="usage-schedule",stream=stdout)
                                                                                
 Usage: carbon_guard schedule [OPTIONS]                                         
                                                                                
 Find the lowest carbon time.                                                   
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ *  --within                     HUMAN_READABLE_DURATI  Time period to        │
│                                 ON                     predict the lowest    │
│                                                        intensity within      │
│                                                        [env var: WITHIN]     │
│                                                        [default: None]       │
│                                                        [required]            │
│    --data-source                [file|national-grid-e  Where to read carbon  │
│                                 so-carbon-intensity]   intensity data from   │
│                                                        [env var:             │
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
│    --national-grid-eso-…        HTTP_OR_HTTPS_URL      URL for the National  │
│                                                        Grid ESO Carbon       │
│                                                        Intensity API         │
│                                                        [env var:             │
│                                                        NATIONAL_GRID_ESO_CA… │
│                                                        [default:             │
│                                                        https://api.carbonin… │
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
uv run carbon_guard check --max-carbon-intensity=999
```

``` ,verify(script_name="carbon_threshold_exceeded", stream=stdout)
Carbon intensity is 1000 gCO2eq/kWh, which is above the max of 999 gCO2eq/kWh
```

You may also return a successful exit code even on high carbon intensity by passing the `--advise-only` flag.

```shell,script(name="carbon_threshold_exceeded_and_skipped",  expected_exit_code=0)
carbon_intensity_is 1000
uv run carbon_guard check --max-carbon-intensity=999 --advise-only
```

Comparing carbon levels with the expected outcome for low carbon intensity:

```shell,script(name="carbon_threshold_ok",  expected_exit_code=0)
carbon_intensity_is 999
uv run carbon_guard check --max-carbon-intensity=999
```

``` ,verify(script_name="carbon_threshold_ok", stream=stdout)
Carbon intensity is 999 gCO2eq/kWh, which is below or equal to the max of 999 gCO2eq/kWh
```

## Data Sources

* [National Grid ESO Carbon Intensity](#national-grid-eso-carbon-intensity)
* [CO2 Signal](#co2-signal)

You may change the data source by specifying the `--data-source` flag.

## National Grid ESO Carbon Intensity

Using the [national-grid-eso-carbon-intensity data source](https://carbonintensity.org.uk/).
[**note**] this only supplies data for the United Kingdom.

```shell,script(name="national_grid_eso_carbon_threshold_ok",  expected_exit_code=0)
uv run carbon_guard check --data-source national-grid-eso-carbon-intensity --max-carbon-intensity=100000
```

``` ,skip()
Carbon intensity is 98 gCO2eq/kWh, which is below or equal to the max of 100000 gCO2eq/kWh
```

You can use this data provider to schedule find the forecasted lowest carbon intensity within a given time period.

```shell,script(name="national_grid_eso_carbon_threshold_ok",  expected_exit_code=0)
uv run carbon_guard schedule --data-source national-grid-eso-carbon-intensity --within "1 hour"
```

``` ,skip()
2023-07-07T09:30:00+00:00
```

### CO2 Signal

Using the [co2-signal data source](https://www.co2signal.com/)
[**note**] This data source requires an account (free/paid) which will supply an API key for usage, and does not support forecasting.

```shell,script(name="co2-signal-carbon-threshold-ok",  expected_exit_code=0)
# export CO2_SIGNAL_API_KEY=<your_api_key_here>
uv run carbon_guard check --data-source co2-signal --max-carbon-intensity=100000 --co2-signal-country-code=GB
```

``` ,skip()
Carbon intensity is 107 gCO2eq/kWh, which is below or equal to the max of 100000 gCO2eq/kWh
```

#### Errors

if you don't provide a `co2-signal-country-code` the call will fail.

```shell,script(name="co2-signal-no-country-code-error",  expected_exit_code=1)
# export CO2_SIGNAL_API_KEY=<your_api_key_here>
uv run carbon_guard check --data-source co2-signal --max-carbon-intensity=100000
```

``` ,verify(script_name="co2-signal-no-country-code-error", stream=stdout)
No country code provided to CO2 Signal Api.
```

if you don't provide a `co2-signal-api-key` the call will fail.

```shell,script(name="co2-signal-no-api-key-error",  expected_exit_code=1)
export CO2_SIGNAL_API_KEY=""
uv run carbon_guard check --data-source co2-signal --max-carbon-intensity=100000 --co2-signal-country-code=GB
```

``` ,verify(script_name="co2-signal-no-api-key-error", stream=stdout)
No API key found for CO2 Signal API.
```

## Adding to your pipelines

This tool is intended to be run inside a pipeline to either fail or skip steps within, based on the current carbon
intensity levels.

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

Alternatively if you want to simply skip a step if the carbon intensity is too high you can use the `continue-on-error`
flag.

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
pip install carbon-guard
carbon_guard --help
```
