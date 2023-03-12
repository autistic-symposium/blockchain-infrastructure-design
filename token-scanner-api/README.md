## token scanner api and cli


<br>

#### installing dependencies

create a venv, either using virtualenv, pipenv, or poetry.

because of some of the dependencies in this code, we will be developing on a python3.9 environment (install here if you don’t have that version on disk):

```
virtualenv -p /usr/local/bin/python3.9 venv
source venv/bin/activate
pip3 install -r requirements.txt
```


<br>

#### add environment variables

now, create an .env file and add an RPC_PROVIDER_URL to connect to ethereum mainnet nodes (you can pick from any of this list of nodes as a service):

```
cp .env.example .env
vim .env
```

<br>

#### installing the package

```
make install
indexer -h
```

<br>

#### deploying on production

we use vercel to deploy this app at .

to deploy new changes, first install vercel:

```
yarn
```

then run:

```
vercel login
vercel .
```