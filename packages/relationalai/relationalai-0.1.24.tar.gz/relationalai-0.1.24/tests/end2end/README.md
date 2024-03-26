# End2End Tests

Tests which

1. Create an engine
2. Run some tests
3. Delete the engine

## Config

### `raiconfig.toml`

If you have a `raiconfig.toml` file, it'll use that, including using the
engine specified in the file.

### Env Vars

Otherwise, it'll authenticate with keys supplied as environment variables,
and create a new engine just for the test session.

Set these variables in the environment (credentials to run against):

```
export RAI_CLIENT_SECRET=...
export RAI_CLIENT_ID=...
```

## Invocation

(After activating the virtual env)

```
$ pytest -s tests/end2end
```
