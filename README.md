# NLP Service

This service provides some Natural Language Processing (NLP) functionalities used in our system.

## APIs

`GET /docsim`: Calculate the similarity between two pieces of text.

Request parameters:

- `a`: first piece of text
- `b`: second piece of text
- `model`: language model in use, currently only `'news'` is available.

Response (JSON):

A scalar floating point value representing the similarity, ranging from 0.0 (completely irrelevant) to 1.0 (exactly the same).

--

`POST /docsim_1ton`: Compute similarity for one piece of text with many.

Request body should be in JSON, with the following fields:

- `one` (string): the pivot
- `many` (list of strings): the candidates to be compared
- `model` (string): the same as for `GET /docsim` API

Response (JSON):

A list of length the same as the length of the input array `many`, each with a floating point value representing the similarity between the pivot and
the corresponding text from many.

--

`POST /ner`: Extract a entity name (usually a company) from a sentence (usually a news title)

Request parameters:

- `q`: the sentence
- `threshold` (float [0,1]):, default to be 0.5, indicating how high probability should take for a single character be considered in a part of the entity name. higher value corresponds to lower false positive rate, while lower value corresponds to lower false negative rate.
- `return_raw` (1 or 0, optional): whether return a list of probability of each character being a part of the entity name

Response (JSON):

- `entity` (a string or null): representing the entity extracted
- `threshold`: same as the value passed in
- `positive_confidence` (float [0,1], or null): how confident the algorithm feels about the entity found; if no entity is found, this field will be null
- `overall_confidence` (float [0,1]): how confidence the algorithm feels about all the character been classified correctly
- `raw` (list of pairs): only present when requested with `return_raw`; each pair contains a character and the probability for that character being a part of the entity name

