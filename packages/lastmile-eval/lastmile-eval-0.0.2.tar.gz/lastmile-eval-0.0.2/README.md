# LastMile AI Eval

An API to measure evaluation criteria (ex: faithfulness) of generative AI outputs.

Particularly, we evaluate based on this triplet of information:

1. User query
2. Data that goes into the LLM
3. LLM's output response

The method `get_rag_eval_scores()` takes in these 3 arguments (and other ones like `api_token`) and outputs a faithfulness score between 0 to 1.

## Usage

To use this library, add this to your code, replacing `queries`, `data`, and `responses` with your own values.

```python
import dotenv
import os

from lastmile_eval.rag import get_rag_eval_scores

statement1 = "the sky is red"
statement2 = "the sky is blue"

queries = ["what color is the sky?", "is the sky blue?"]
data = [statement1, statement1]
responses = [statement1, statement2]
api_token = <lastmile-api-token>

result = get_rag_eval_scores(
  queries,
  data,
  responses,
  api_token,
)

# result will look something like:
# {'p_faithful': [0.9955534338951111, 6.857347034383565e-05]}
```

## LastMile API token

To get a LastMile AI token, please go to the [LastMile token's webpage](https://lastmileai.dev/settings?page=tokens).
You can create an account with Google or Github and then click the "Create new token" in the "API Tokens" section. Once a token is created, be sure to save it somewhere since you won't be able to see the value of it from the website again (though you can create a new one if that happens).

**Please be careful not to share your token on GitHub**. Instead we recommend saving it under your project’s (or home directory) `.env` file as: `LASTMILE_API_TOKEN=<TOKEN_HERE>`, and use loadenv instead:

```bash
pip3 install python-dotenv
```

```python
import dotenv
import os

dotenv.load_dotenv()
api_token = os.getenv("LASTMILE_API_TOKEN")
```
