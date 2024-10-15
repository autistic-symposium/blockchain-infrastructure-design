## design of a protocol for management and bartering of game (NFT) assets

<br>

### I. introduction

<br>

we leverage the principles of [simplicity first](http://principles-wiki.net/principles:gall_s_law), [composability](https://a16zcrypto.com/posts/article/composability-is-to-software-as-compounding-interest-is-to-finance/), and extensibility to design a plan to implement an end-to-end (first version of a) marketplace protocol for managing game NFT assets.

<br>

<p align="center">
<img src="https://github.com/go-outside-labs/blockchain-infrastructure-design/assets/138340846/74456b31-d8c1-4462-8fb8-d303c51a3cd5" width="80%" align="center"/>


<br>
<br>

our protocol is designed to take advantage of non-fungible tokens (*i.e.*, EVM’s compatible standards such as [ERC-721](https://ethereum.org/en/developers/docs/standards/tokens/erc-721), [ERC-1155](https://ethereum.org/en/developers/docs/standards/tokens/erc-1155), and extensions) for game assets, which includes **ownership** (the address that holds the token or the), provable [scarcity](https://vitalik.eth.limo/general/2021/03/23/legitimacy.html) (through rarity traits and authenticity), [interoperability](https://www.playtoearn.online/whats-interoperability/), and **emitting events** when the state changes.

storage and computation costs are expensive and restricted on the ethereum blockchain. to overcome the challenges regarding **searching, sorting, notification**, and **bartering**, our **hybrid design contains both on-chain and off-chain components**. 
 
in addition, the [blockchain trilemma](https://vitalik.eth.limo/general/2021/04/07/sharding.html) states that only two can be guaranteed among: decentralization, security, and scalability (similarly to the broader [CAP theorem](https://en.wikipedia.org/wiki/CAP_theorem)). since ethereum communities emphasize that [decentralization](https://onezero.medium.com/why-decentralization-matters-5e3f79f7638e) and security are prerogatives, we design a solution that improves scalability through an **off-chain microservice infrastructure** (which can be deployed in a cloud service such as [AWS](https://aws.amazon.com/), [GCP](https://cloud.google.com/?hl=en), [azure](https://azure.microsoft.com/en-us/), [vercel](https://vercel.com/), etc.).

while these choices might initially compromise certain aspects of decentralization of the protocol, our **modular design** allows for gradual improvements and [progressive decentralization](https://a16zcrypto.com/posts/article/progressive-decentralization-crypto-product-management/) in future versions that could take full advantage of blockchain technologies, for instance, by exploring layer-2 strategies.

In the subsequent sessions, we discuss the design and roadmap for our protocol, concluding with a survey on improvements, roads not taken, and their merits and demerits.

<br>

----

<br>

### II. assumptions

<br>

we make the following assumptions in our design:

<br>

* the **game's assets smart contracts are already available in another protocol and platform**, which we have access to through the blockchain APIs.

<br>

* the player already has a **digital wallet on which the assets are minted to**. the assets are not [soulbound](https://vitalik.ca/general/2022/01/26/soulbound.html), *i.e.,* they can be transferable.

<br>

* the game's assets smart contracts contain (immutable) **metadata that indicates an asset's rarity and utility** (*e.g.,* name, category, permanent URL for thumbnail, traits, required level). 
    - our protocol will use this data to calculate a "rating" for the asset, which facilitates bartering (illustrated in the frontend sketch as a 1-5 stars rating).
    - the algorithm calculating this rating is out of the scope of this document, but we incorporated it into our modular microservice infrastructure.

<br>

* although this is a high-level design and we won't explicitly specify our protocol's smart contracts, they should contain **two mutable `boolean` variables** (or a logic variation):
    - `EQUIPPED`: specifying that the player's avatar is wearing the asset. this variable should be in sync with the game's main protocol.
    - `FOR_TRADE`: specifying that the player has marked the asset for bartering. 
    
<br>

* as our protocol only focuses on bartering, the original asset's smart contracts have **no logic for secondary market fee**s (or are irrelevant in our context).

<br>

* our protocol's smart contracts contain **logic for a marketplace's fee in each barter transaction**, and this is the only fee we consider in this design.

<br>

----

<br>


### III. protocol layers

<br>
<br>

<p align="center">
<img src="https://github.com/go-outside-labs/blockchain-infrastructure-design/assets/138340846/7ece4870-3383-44a8-b9bc-4404d1327a5d" width="100%" align="center"/>


<br>
<br>

the **frontend layer** should provide the functions sketched in figure 1, consisting of a simple dashboard that can be built on a **javascript/typescript framework**:

* the only extra complexity is the **integration with browser wallets**. 

* **signning up or logging in should leverage the game's original protocol** or simply be **achieved through the user's wallet**, as we are not creating a separate profile database or gathering personal data for the user.

<br>

the **backend layer** consists of:

* a **database solution to track bartering operations** (*e.g.*, a noSQL such as [mongoDB](https://www.mongodb.com/) or an RDBMS supporting big data). 
    - in the simplest form, every time a user places a bartering bid on an asset, the database could create an entry with the asset's and the user's `address` (or `tokenId`). this entry would be deleted when the bid is refused or accepted.
    - this approach could be later replaced by decentralized alternatives (*e.g.,* [kwil](https://www.kwil.com/), [orbitDB](https://orbitdb.org/), [bigchainDB](https://www.bigchaindb.com/), [convenantSQL](https://developers.covenantsql.io/docs/en/intro), [ceramic](https://ceramic.network/)).

* an **orchestration infrastructure**, through a [kubernetes](https://kubernetes.io/) solution written on [terraform](https://www.terraform.io/).

* **microservices** for off-chain **searching and sorting** (*e.g.*, [ELK](https://aws.amazon.com/what-is/elk-stack/), [biguery](https://cloud.google.com/bigquery/), [cloudsearch](https://aws.amazon.com/cloudsearch/), [hive](https://hive.apache.org/)), **notification system** (*e.g.*, a simple cloud messaging service such as [AWS SNS](https://aws.amazon.com/sns/) or a more elaborated pub/sub solution such as [AWS SQS](https://aws.amazon.com/sqs/), [Kafka](https://kafka.apache.org/), [ZeroMQ](https://zeromq.org/), [AWS Kinesis](https://aws.amazon.com/kinesis/), [RabbitMQ](https://rabbitmq.com/)), and an **asset rating evaluation** (through an in-house algorithm leveraging the assets' traits as input).

* a **CI/CD pipeline** (*e.g.*, [jenkins](https://www.jenkins.io/), [circleci](https://circleci.com/), [gitHub actions](https://github.com/features/actions)).

* depending on the scale of the project, we might want to rely on something other than [blockchain data availability](https://ethereum.org/en/developers/docs/data-availability), so we could consider adding a **database to cache the smart contract events and keep track of ownership** (*e.g.*, [Redis](https://redis.io/)). This extra step is included in the roadmap below.

* likewise, any gateway and CDN solution should be incorporated in this layer.
    
<br>

finally, the **blockchain layer** contains our protocol smart contracts and their test suites. a multi-signature wallet (*e.g.,* [gnosis](https://www.gnosis.io/)) could be leveraged to enhance the security of this deployment.

<br>

<p align="center">
<img src="https://github.com/go-outside-labs/blockchain-infrastructure-design/assets/138340846/803d2e05-6e06-46c0-afd7-ef05c0010ece" width="100%" align="center"/>


<br>
<br>

----

<br>

### IV. implementation roadmap

<br>
<br>

<p align="center">
<img src="https://github.com/go-outside-labs/blockchain-infrastructure-design/assets/138340846/a857cacc-811e-43db-9b7b-eca99ff1c8a7" width="100%" align="center"/>

<br>
<br>

----

<br>

### V. roads not taken in our approach

<br>

#### a full on-chain narketplace for auctions with a native token

<br>

ideally, a marketplace should use smart contracts to fully control asset auctions and transactions. examples of this approach are [sandbox](https://www.sandbox.game/en/) or [axie infinite marketplace's contract for auction](https://etherscan.io/address/0xf4985070ce32b6b1994329df787d1acc9a2dd9).

however, since we are only focusing on bartering, this solution is overkill as creating a new token brings several challenges, such as extra engineering resources, adoption, tokenomics design, and security concerns. 

<br>

#### a full on-chain decentralized autonomous bartering algorithm

<br>

in general, finding [multiple "coincidence of wants"](https://www.geeksforgeeks.org/what-is-barter-system-and-double-coincidence-of-wants/) of various assets translates to finding hypercycles in directed hypergraphs (an [NP-complete](https://en.wikipedia.org/wiki/NP-completeness) problem). Therefore, the bartering problem in a distributed setting is similar to [dijkstra’s banker’s problem](https://en.wikipedia.org/wiki/Banker's_algorithm).

<br>

<p align="center">
<img src="https://github.com/go-outside-labs/blockchain-infrastructure-design/assets/138340846/5df0628e-8fef-4625-8e9f-e83a878fad81" width="40%" align="center"/>



<br>
<br>

an on-chain implementation of this algorithm is tricky. In its most naive form, the design could be costly and probably prone to tampering, fraud, and MEV exploitation. in addition, it would need to assume a large amount of simultaneous trades.

<br>

#### a coincidence-of-wants bartering algorithm with off-chain batches

instead of leveraging an off-chain database solution, we could move our bartering logic on-chain by implementing a system for "coincidence of wants" with batch transfers. 

in this approach, when multiple [intents](https://www.paradigm.xyz/2023/06/intents) for the same asset are within a batch, there could be an opportunity for a peer-to-peer swap that doesn't rely on the main network.

a successful example in DeFi is the [cowswap](https://cow.fi/) protocol, which collects and aggregates intents off-chain, setting them on batches. the batches are run by third-party solvers.

this design would need to assume a large number of trades at the same time and that there will be willed solvers (or an extra in-house structure) to run the batches.

<br>

#### an NFT-focused chain or L2


a few successful decentralized game platforms (such as [enjin](https://enjin.io/) and [immutable](https://www.immutable.com/)) have adopted an NFT-focused chain or L2 solution to customize the process of multiple NFT transfers, tracking metadata and provenance, facilitating intellectual property, and interoperability among chains. 

however, there is a massive overhead to building, maintaining, governing, and creating the adoption of a new blockchain and a native token, making this solution unsuitable for our bartering protocol.
