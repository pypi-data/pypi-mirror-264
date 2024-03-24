# langfuse-web

Not all of the methods you might need for interacting with Langfuse are
available through their API library. This makes use of `requests.Session` to use
the web interface pull all prompts and delete prompts.

### Functions

- `get_all_prompts`
- `delete_prompt`
