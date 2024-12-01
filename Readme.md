# Автоматизация отчетности ВКР

Автоматическая генерация отчёта по ВКР.

```shell
docker build -t document-builder .

```

```shell
docker run --rm -v $PWD/output:/output -v $PWD/input:/app document-builder

```
