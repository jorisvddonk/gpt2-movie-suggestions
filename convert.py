import os
from markdown import Markdown
from io import StringIO
from tqdm import tqdm
import jsonlines


def unmark_element(element, stream=None):
    if stream is None:
        stream = StringIO()
    if element.text:
        stream.write(element.text)
    for sub in element:
        unmark_element(sub, stream)
    if element.tail:
        stream.write(element.tail)
    return stream.getvalue()


# patching Markdown
Markdown.output_formats["plain"] = unmark_element
__md = Markdown(output_format="plain")
__md.stripTopLevelTags = False


def unmark(text):
    return __md.convert(text)


out = open('./data.txt', 'w', encoding="utf8")
num = 0

for f in os.listdir("./data"):
    with jsonlines.open(os.path.join("./data", f)) as reader:
        for data in tqdm(reader.iter(type=dict, skip_invalid=True)):
        entry = "<REQUEST>\n%s\n%s\n\n<REPLY>\n%s\n\n<END>\n\n" % (
            data['title'], unmark(data['selftext']), unmark(data['body']))
        out.write(entry)
        num += 1

print(num)
out.close()
