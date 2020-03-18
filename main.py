from fastapi import FastAPI
from starlette.responses import HTMLResponse
import gpt_2_simple as gpt2
from pydantic import BaseModel
from datetime import datetime
import re

sess = gpt2.start_tf_sess()
gpt2.load_gpt2(sess, run_name='run1')


def generate_texts(text: str):
    actual_text = "<REQUEST>\n%s\n\n<REPLY>\n" % text
    with sess.graph.as_default():
        datas = gpt2.generate(sess,
                              length=250,
                              temperature=0.7,
                              prefix=actual_text,
                              nsamples=5,
                              batch_size=5,
                              run_name='run1',
                              return_as_list=True
                              )
        retval = {
            "raw": [],
            "text": []
        }
        for data in datas:
            retval["raw"].append(data)
            m = re.search("\\<REQUEST\\>(.*)\\<REPLY\\>(.*?)\\<(REQUEST|REPLY|END)\\>",
                          "%s<END>" % data, re.MULTILINE | re.DOTALL)
            actual_text = m.group(2).strip()
            retval["text"].append(actual_text)
        return retval


class Input(BaseModel):
    text: str


app = FastAPI()
indexhtml = open('./index.html', 'r').read()


@app.get("/.*", include_in_schema=False)
def root():
    return HTMLResponse(indexhtml)


@app.post("/generate")
def generate(data: Input):
    data = generate_texts(data.text)
    return {"data": data['text'], "raw": data['raw']}
