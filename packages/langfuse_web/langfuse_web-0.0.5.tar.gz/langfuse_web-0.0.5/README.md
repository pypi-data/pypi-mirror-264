# langfuse-web

Not all of the methods you might need for interacting with Langfuse are
available through their API library. This makes use of `requests.Session` to use
the web interface pull all prompts and delete prompts.

### Functions

- `get_all_prompts`
- `delete_prompt`

### Setup

The following environment variables are expected to exist:
```
LANGFUSE_HOST
LANGFUSE_PROJECT
LANGFUSE_EMAIL
LANGFUSE_PASSWORD
```

`pip3 install python-dotenv` and employing an `.env` file is a method frequently
employed to manage this requirement
