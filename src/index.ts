#!/bin/env node
import axios from "axios";
import BigNumber from "bignumber.js";
import yargs from "yargs";
import { hideBin } from "yargs/helpers";

import { Transaction } from "./types";

yargs(hideBin(process.argv))
  .command(
    "get-airdrop-tx <hash>",
    "Grab airdrop tx metadata",
    (yargs) =>
      yargs
        .option("hash", {
          type: "string",
          description: "Transaction hash",
          demandOption: true,
        })
        .option("node", {
          type: "string",
          description: "REST node to reach",
          default: "https://osmosis.rest.stakin-nodes.com",
        }),
    async (argv) => {
      const { node, hash } = argv;
      const api = axios.create({ baseURL: node });
      try {
        const res = await api.get<{ tx: Transaction }>(`/cosmos/tx/v1beta1/txs/${hash}`);
        const { tx } = res.data;
        const total = tx.body.messages.reduce(
          (acc, cur) => acc.plus(cur.amount[0]!.amount),
          BigNumber(0),
        );
        const data = tx.body.messages.map((msg) => {
          const amount = BigNumber(msg.amount[0]!.amount);
          return {
            address: msg.to_address,
            amount: amount.toFixed(),
            share: amount.dividedBy(total).toString(),
          };
        });
        console.log(data);
      } catch (e) {
        if (axios.isAxiosError(e)) {
          console.log(e.response?.data);
        }
      }
    },
  )
  .demandCommand(1)
  .parse();
