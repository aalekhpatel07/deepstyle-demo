# DeepStyle

A fine-tuned [DBert model](https://aclanthology.org/2020.wnut-1.30.pdf) that can be used to extract vector embeddings (of dimension `768`) for short text articles.

> Note: The embeddings are of dimension `768`, and use the `cosine` similarity measure.

## Usage

```sh
docker compose up -d
```

*Note*: This repo wraps [hayj/DeepStyle](https://github.com/hayj/DeepStyle) into a [FastAPI](https://fastapi.tiangolo.com/) web server and adds a [Qdrant](https://qdrant.tech/) next to it in a docker compose setup.

