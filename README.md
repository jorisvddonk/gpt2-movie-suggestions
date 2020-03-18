# GPT-2 movie suggestions

This repository contains a simple webapp and GPT-2 model to get movie suggestions! The model is trained on more than 4 years' worth of data from the [MovieSuggestions subreddit](https://www.reddit.com/r/MovieSuggestions/). Made using gpt-2-simple (via [Max Woolf's guide](https://minimaxir.com/2019/09/howto-gpt2/)).

## Running locally

0. Clone this repository
1. Download [the latest release](https://github.com/jorisvddonk/gpt2-movie-suggestions/releases/download/1.0.0/model.tar) and extract it to the `model` folder
2. Build the container: `docker build . -t gpt2-moviesuggestions`
3. Run the container: ``docker run --rm -it -p 8000:8000 -v ${PWD}/model:/model feltyrion-gpt2`
4. navigate to http://localhost:8000/ and explore!


## Finetuning your own model

First, you need to get all required data. Someone has exported a bunch of Reddit data to BigQuery, which is available in a public dataset. Run the following query:

```
WITH posts AS
(
  SELECT title, selftext, id FROM `fh-bigquery.reddit_posts.2*` WHERE subreddit = 'MovieSuggestions'
  AND selftext != '[removed]' AND selftext != '[deleted]'
  AND _TABLE_SUFFIX BETWEEN '015_01' AND '019_10'
),
comments AS (
  SELECT body, parent_id
  FROM `fh-bigquery.reddit_comments.2*` 
  WHERE subreddit = 'MovieSuggestions'
  AND body != '[removed]' AND body != '[deleted]'
  AND _TABLE_SUFFIX BETWEEN '015_01' AND '019_10'
)

SELECT title, selftext, body FROM posts JOIN comments ON comments.parent_id = CONCAT('t3_', posts.id)
```

then export the data somewhere as JSON and download it. Rename the JSON file to `input.json` and put it in the `data` folder.

Next, run `convert.js` to convert the JSON to a plaintext file suitable for training.

Finally, follow [Max Woolf's guide](https://minimaxir.com/2019/09/howto-gpt2/) to finetune GPT-2 using the dataset!
