from fastapi import FastAPI
from starlette.responses import HTMLResponse
import gpt_2_simple as gpt2
from pydantic import BaseModel
from datetime import datetime

sess = gpt2.start_tf_sess()
gpt2.load_gpt2(sess, run_name='run1')


def generate_text(text: str):
    actual_text = "<REQUEST>\n%s\n\n<REPLY>\n" % text
    with sess.graph.as_default():
        return gpt2.generate(sess,
                             length=250,
                             temperature=0.7,
                             prefix=actual_text,
                             nsamples=1,
                             batch_size=1,
                             run_name='run1',
                             return_as_list=True
                             )[0]


class Input(BaseModel):
    text: str


app = FastAPI()
indexhtml = open('./index.html', 'r').read()


@app.get("/.*", include_in_schema=False)
def root():
    return HTMLResponse(indexhtml)


@app.post("/generate")
def generate(data: Input):
    return {"data": generate_text(data.text)}