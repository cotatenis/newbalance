
░█████╗░░█████╗░████████╗░█████╗░████████╗███████╗███╗░░██╗██╗░██████╗
██╔══██╗██╔══██╗╚══██╔══╝██╔══██╗╚══██╔══╝██╔════╝████╗░██║██║██╔════╝
██║░░╚═╝██║░░██║░░░██║░░░███████║░░░██║░░░█████╗░░██╔██╗██║██║╚█████╗░
██║░░██╗██║░░██║░░░██║░░░██╔══██║░░░██║░░░██╔══╝░░██║╚████║██║░╚═══██╗
╚█████╔╝╚█████╔╝░░░██║░░░██║░░██║░░░██║░░░███████╗██║░╚███║██║██████╔╝
░╚════╝░░╚════╝░░░░╚═╝░░░╚═╝░░╚═╝░░░╚═╝░░░╚══════╝╚═╝░░╚══╝╚═╝╚═════╝░


--------------------------------------------------------------------------

# Web crawler

url: [https://www.newbalance.com.br/](https://www.newbalance.com.br/)

# 1. Configuration
Before you run this project and for the proper running of this program you need to set up some variables inside `newbalance/newbalance/settings.py`.

## 1.1 SENTRY
This project utilizes [SENTRY](https://sentry.io/) for error tracking.

- `SPIDERMON_SENTRY_DSN`
- `SPIDERMON_SENTRY_PROJECT_NAME`
- `SPIDERMON_SENTRY_ENVIRONMENT_TYPE`

## 1.2 GOOGLE CLOUD PLATFORM

- `GCS_PROJECT_ID` 
- `GCP_CREDENTIALS`
- `GCP_STORAGE`
- `GCP_STORAGE_CRAWLER_STATS`
- `IMAGES_STORE`

## 1.3 DISCORD
- `DISCORD_WEBHOOK_URL`
- `DISCORD_THUMBNAIL_URL`
- `SPIDERMON_DISCORD_WEBHOOK_URL`


# 2. Implemented Brands
- awin_newbalance [`NewBalanceSpider`]

# 3. Build

```shell
cd newbalance
make docker-build-production
```

# 4. Publish

```shell
make docker-publish-production
```

# 5. Use

```shell
docker run --shm-size="2g" gcr.io/cotatenis/cotatenis-crawl-awin-newbalance:0.1.3
```
