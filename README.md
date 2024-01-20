## voucher backend
### build docker image

```shell script
docker build -t moneyro_backend . --build-arg VERSION=2.2
```

#### run tests
```shell script
docker compose run backend test --settings=runner.settings_test
```
