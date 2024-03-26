import json
import logging
import os
import sys

import requests
from redact import redact_string

logging.basicConfig()
log = logging.getLogger("langfuse_web")
log.setLevel(level=logging.DEBUG)


class LangfuseWebEnv(object):
    def __init__(self):
        """
        Get the Langfuse environment varibles
        """

        self.host = os.getenv("LANGFUSE_HOST")
        self.project = os.getenv("LANGFUSE_PROJECT")
        self.email = os.getenv("LANGFUSE_EMAIL")
        self.password = os.getenv("LANGFUSE_PASSWORD")

    def __str__(self):
        return (
            f"project: {self.project}, email: {self.email}, "
            f"password: {redact_string(self.password)}"  # type:ignore
        )


class LFWebSession(object):
    def __init__(self):
        log.debug("initializing the Langfuse web session")

        self.env = LangfuseWebEnv()
        self.session = requests.Session()

        log.debug(self.env)

        log.debug("getting csrf token")
        res = self.session.get(f"{self.env.host}/api/auth/csrf")
        csrf = res.json()
        if "csrfToken" not in csrf:
            log.critical("csrf token not in response")
            sys.exit(1)
        log.debug(f"got CSRF token {csrf['csrfToken']}")

        # auth blob
        data = {
            "email": self.env.email,
            "password": self.env.password,
            "callbackUrl": "/",
            "redirect": "false",
            "csrfToken": csrf["csrfToken"],
            "json": "true",
        }

        log.debug("attempting to login")
        log.debug(f"login data: {json.dumps(data)}")
        res = self.session.post(
            f"{self.env.host}/api/auth/callback/credentials",
            json=data,
            allow_redirects=False,
        )

        # post auth
        log.debug(f"status code: {res.status_code}")
        log.debug(f"response text {res.text}")

        # get session details
        log.debug("attempting to get session details")
        res = self.session.get(f"{self.env.host}/api/auth/session")
        log.debug(f"status code: {res.status_code}")
        log.debug(f"response text {res.text}")
        info = res.json()

        id = ""
        for p in info["user"]["projects"]:
            if p["name"] == self.env.project:
                id = p["id"]
                break
        if id == "":
            log.critical(f"langfuse project '{self.env.project}' was not found")
            sys.exit(1)

        log.debug(f"project ID for '{self.env.project}' is {id}")

        self.project_id = id

    def __enter__(self):
        log.debug("entering Langfuse web context")
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        log.debug("automatically closing Langfuse web session")
        self.session.close()


def get_all_prompts():
    with LFWebSession() as lfws:
        input = {"0": {"json": {"projectId": lfws.project_id}}}
        compact = json.dumps(input).replace(" ", "")
        log.debug(f"compacted request string: {compact}")
        url = f"{lfws.env.host}/api/trpc/prompts.all?batch=1&input={compact}"
        log.debug(f"getting prompts from {url}")
        res = lfws.session.get(url)
        log.debug(f"status code: {res.status_code}")
        log.debug(f"response text {res.text}")

        return res.json()


def delete_prompt(name: str):
    with LFWebSession() as lfws:
        url = f"{lfws.env.host}/api/trpc/prompts.delete?batch=1"

        data = {
            "0": {"json": {"projectId": f"{lfws.project_id}", "promptName": f"{name}"}}
        }
        try:
            # as long as the call is made correctly, this will return a 200,
            # even if the prompt does not exist
            res = lfws.session.post(url, json=data)
            log.debug(f"deletion of {name} status code: {res.status_code}")
            log.debug(f"response text {res.text}")
        except Exception as e:
            log.warning(f"something went wrong: {e}")


if __name__ == "__main__":
    print(json.dumps(get_all_prompts))
