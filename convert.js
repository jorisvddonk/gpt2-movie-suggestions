const removeMd = require('remove-markdown');
const jsonlines = require('jsonlines');
const parser = jsonlines.parse();
const fs = require('fs');

const entries = [];
let numi = 0;
parser.on('data', function (data) {
  const entry = `<REQUEST>\n${data.title}\n${removeMd(data.selftext)}\n\n<REPLY>\n${removeMd(data.body)}\n\n<END>\n\n`
  entries.push(entry);
  numi += 1;
  if (numi % 1000 == 0) {
    console.log(numi);
  }
})

parser.on('end', function () {
  fs.writeFileSync('./data_.txt', entries.join('\n'));
})

const stream = fs.createReadStream("./data/input.json", { encoding: 'utf8' });
stream.pipe(parser);