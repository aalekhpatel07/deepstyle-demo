#!/usr/bin/env python
import pathlib
import typing
from threading import Lock
from contextlib import asynccontextmanager

import deepstyle
from deepstyle.model import DeepStyle
import numpy as np

from fastapi import FastAPI
from pydantic import BaseModel

class Text(BaseModel):
    text: str

class Embeddings(BaseModel):
    embeddings: typing.List[float]

model = None
model_lock = None

app = FastAPI()


@asynccontextmanager
async def lifespan(app: FastAPI):
    global model
    global model_lock

    full_path = pathlib.Path("/model")
    model = DeepStyle(str(full_path.absolute()))
    model_lock = Lock()
    yield
    del model


app = FastAPI(lifespan=lifespan)


@app.post("/")
async def get_embeddings(text: Text) -> Embeddings:
    """Get embeddings for the text using DBert-ft model

    """
    global model
    global model_lock

    with model_lock:
        embeddings = model.embed(text.text)
        return Embeddings(embeddings=embeddings.tolist())

