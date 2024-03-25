# Cuckoo

Cuckoo is a price alarm tool for assets. It can track the price of the asset you desire using various data sources such as Coingecko and Geckoterminal. Once an asset you are monitoring reaches the target price you set, Cuckoo will send you a message.

## Setup

Ensure you have Python 3.10 or above installed. You can download and install (or update to) the latest release of Cuckoo with the following command:

```
pip install t2og-cuckoo
```

Alternatively, you can pull and install the latest version from this repository using the following command:

```
pip install git+https://github.com/t2og/cuckoo.git
```

## Configuration

There are two types of configuration: environment variables to configure Cuckoo, and a watchlist config where you can specify what assets you want to track the price of when using Config-based usage.

For sending messages, you have the flexibility to either use your own email server or leverage the Gmail API.

To use your own email server, set the following environment variables:

```
SMTP_SERVER=mail.yourdomain.com
SMTP_PORT=587
SMTP_USER=info
SMTP_PASSWORD=password
SMTP_EMAIL=info@yourdomain.com
```

Alternatively, if you prefer to use the [Gmail API](https://developers.google.com/gmail/api/quickstart/python), set the following environment variables:

```
GMAIL_TOKEN=token.json
GMAIL_FROM=yourname@gmail.com
```

The default refresh time is 6 minutes; however, you can modify this interval through the following environment variables. For instance, setting it to refresh the data every 30 seconds can be done as shown below:

```
REFRESH_MINUTES=0.5
```

> [!NOTE]
> Setting the refresh interval too low may result in an **Error 429** due to rate limits imposed by CoinGecko or other data sources.

## Command-line usage

For instance, if you want to track the price of Bitcoin and ETH, and receive a message when ETH's price hits 3800, you can input the following command:

```
cuckoo --watch_tokens bitcoin,ethereum --check_token ethereum --checker higher --target_price 3800 --send_mail yourname@domainname.com
```

## Config-based usage

You can create a YAML config file like the following:

```
tokens: 
  - symbol: 
      id: bitcoin
  - symbol: 
      id: bonk
      gt: 0.000030
      lte: 0.000028
  - pool: 
      network: eth
      address: "0x971add32ea87f10bd192671630be3be8a11b8623"
      name: CRV / cvxCRV
      attribute: quote_token_price_base_token
      gte: 0.92
      lte: 0.89
  - pool:
      network: solana
      address: 3ne4mWqdYuNiYrYZC9TrA3FcfuFdErghH97vNPbjicr1
      name: BONK / SOL
      attribute: base_token_price_usd
      gte: 0.000030
      lte: 0.000028

displays: 
    - console:

messengers:
    - console:
    - mail: [yourname@domainname.com]
```
