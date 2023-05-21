export type TransactionMessageAmount = {
  denom: string;
  amount: string;
};

export type TransactionMessage = {
  "@type": string;
  from_address: string;
  to_address: string;
  amount: TransactionMessageAmount[];
};

export type Transaction = {
  body: {
    messages: TransactionMessage[];
    memo: string;
  };
  signatures: string[];
};
