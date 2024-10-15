## 🛠🪙  token scanner api and cli

<br>

##### 👉 this project implements a cli tool that indexes transfer events for a particular token, and is deployed to a restful api for fast balance and ownership statistics retrieval. it utilizes [JSON-RPC methods](https://docs.infura.io/infura/networks/ethereum/json-rpc-methods/eth_getlogs) `eth_blockNumber` and `eth_getLogs`.

##### 🛠 system design for this project:

![blockchain intel - mvp](https://user-images.githubusercontent.com/1130416/224561560-3fd67632-fba6-497c-b3b6-c5c5298701f0.png)

##### 📚 more details can be found in my mirror post, **[quant #3: building a scalable event scanner for ethereum](https://mirror.xyz/go-outside.eth/vSF18xcLyfXLIWwxjreRa3I_XskwgnjSc6pScegNJWI)**.


<br>

---

### setting up 

<br>

#### installing dependencies

because of some of the dependencies in this code, we will be developing on a python3.9 environment (install here if you don’t have that version on disk):

```
virtualenv -p /usr/local/bin/python3.9 venv
source venv/bin/activate
make install_dep
```


<br>

#### adding environment variables

create a `.env` file and add an `RPC_PROVIDER_URL` to connect to ethereum mainnet nodes (for example, from [this list](https://ethereumnodes.com/)):

```
cp .env.example .env
vim .env
```

<br>

#### installing the package

```
make install
```

<br>

----

### running

<br>


```
indexer -h

🪙 Token indexer and API.

optional arguments:
  -h, --help  show this help message and exit
  -e          Retrieve historical transfer events data on Ethereum. Example: indexer -e
  -p PROCESS  Process historical transfer events data. Example: indexer -p <json data file>
  -d DB       Populate db with processed event data. Example: indexer -d <json data file>
  -a          Run the event scanner api locally. Example: indexer -a
  -b BALANCE  Fetch token balance for a given wallet. Example: indexer -b <wallet address>
  -t TOP      Fetch top token holders. Example: indexer -t <number of holders>
```


<br>

---


### deploying in production

<br>

follow [this instructions](https://mirror.xyz/go-outside.eth/vSF18xcLyfXLIWwxjreRa3I_XskwgnjSc6pScegNJWI) to deploy the indexer to [vercel](https://vercel.com/) and [mongodb atlas](https://cloud.mongodb.com/v2/640ec23b5c46a564602b7c0e#/overview).

<br>

