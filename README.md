# Carbon Guard 👮

We are taking the workload to carbon guard (to carbon guard)  to carbon guard


## Usage

```shell,script(name="usage", expected_exit_code=0)
poetry run carbon_guard --help
```

``` ,verify(script_name="usage", stream=stdout)
                                                                                
 Usage: carbon_guard [OPTIONS]                                                  
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                  │
╰──────────────────────────────────────────────────────────────────────────────╯

```

```shell,script(name="carbon_check",  expected_exit_code=0)
poetry run carbon_guard 
```

``` ,verify(script_name="carbon_check", stream=stdout)
Carbon is low!
```