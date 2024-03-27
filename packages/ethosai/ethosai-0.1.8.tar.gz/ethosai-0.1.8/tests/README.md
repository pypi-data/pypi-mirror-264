## Testing: VCR usage

Testing the SDK uses the (vcrpy library)[https://vcrpy.readthedocs.io/en/latest/].

In order to begin testing, you need to use the "make rebuild-everything-from-scratch" command from the ethos main repo root directory. Then you need to create a secrets.env file in src/, that has the following variables:

```
ETHOS_API_KEY=\[your_api_key\]
NAMESPACE_ID=\[your_first_namespace_id\]
PROJECT_ID=\[your_first_project_id\]
```

You'll need to run the tests with `make record` at least once with the app running locally. The HTTP calls will be stored as "cassettes" by vcrpy and `make test` will then run without the app up.
