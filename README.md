# Lottery Combination Lab

Controlled generation, filtering, comparison, selection, and final audit of lottery candidates.

This MVP does not purchase a ticket.

## CLI

```bash
combination-lab generate --game lotto --count 10000
combination-lab filter --input candidates.json --game lotto
combination-lab audit --input candidates.json --game lotto
combination-lab export-final --input candidates.json --game lotto
```
