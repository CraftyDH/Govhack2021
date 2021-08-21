account {
    username varchar(15) unique,
    password varchar(20),
    publicKey varchar(100) unique,
    privateKey varchar(100) unique primary key,
    local_ledger varchar(1000) --chain
}
chain {
    next varchar(1000) NULL, -- chain
    current varchar(1000) -- block
}

block { -- what do we store for proof of stake?
    id primary key int,
    amount int,
	receiverPublicKey varchar,
    senderPublicKey varchar,
    timestamp int
}

