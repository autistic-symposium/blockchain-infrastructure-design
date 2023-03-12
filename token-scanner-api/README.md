## 🛠🪙  token scanner api and cli

<br>

##### 👉 this project implements a cli tool that indexes transfer events for a particular token, and is deployed to a restful api for fast balance and ownership statistics retrieval. this is the first step for training machine learning models on the chains (*e.g.*, high-frequency trading with deep learning).

##### 📚 more details can be found in my mirror post, **[quant #3: building a scalable event scanner for ethereum](https://mirror.xyz/steinkirch.eth/vSF18xcLyfXLIWwxjreRa3I_XskwgnjSc6pScegNJWI)**.

<br>

---

### setting up 

<br>

#### installing dependencies

because of some of the dependencies in this code, we will be developing on a python3.9 environment (install here if you don’t have that version on disk):

```
virtualenv -p /usr/local/bin/python3.9 venv
source venv/bin/activate
pip3 install -r requirements.txt
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


```


<br>

---

### development

<br>

#### deploying in production

we use vercel to deploy this app:

```
vercel login
vercel .
```

<br>

