
import os
import json
import click
import openai as oai



def ensure_directory():
    try:
        os.mkdir(f'{os.environ.get("HOME")}/.chatgpt')
    except:
        pass

def get_api():
    ensure_directory()
    if not os.path.exists(f'{os.environ.get("HOME")}/.chatgpt/api_key'):
        api_key = click.prompt("Please provide an api key")
        with open(f'{os.environ.get("HOME")}/.chatgpt/api_key', "w") as fp:
            fp.write(api_key)

    with open(f'{os.environ.get("HOME")}/.chatgpt/api_key', "r") as fp:
        oai.api_key = fp.readline()
    return oai

def get_conversations():
    ensure_directory()
    try:
        with open(f'{os.environ.get("HOME")}/.chatgpt/history.json', "r") as fp:
            return json.load(fp)
    except FileNotFoundError:
        return {"current": -1, "conversations": []}


def update_conversation(conversation):
    conversations = get_conversations()
    if conversations["current"] == -1:
        conversations["conversations"].append(
            {"summary": conversation[1].get("content"), "messages": conversation}
        )
        conversations["current"] = len(conversations["conversations"]) - 1
    else:
        conversations["conversations"][conversations["current"]][
            "messages"
        ] = conversation
    save_conversations(conversations)


def save_conversations(conversations):
    ensure_directory()
    with open(f'{os.environ.get("HOME")}/.chatgpt/history.json', "w") as fp:
        return json.dump(conversations, fp)


def set_current_idx(idx):
    conversations = get_conversations()
    conversations["current"] = idx
    save_conversations(conversations)


def get_current_conversation():
    conversations = get_conversations()
    current_idx = conversations.get("current")
    if current_idx == -1:
        return [
            {
                "role": "system",
                "content": "You are a computer programming assistant.",
            }
        ]
    return conversations.get("conversations")[current_idx].get("messages")


@click.command()
@click.argument("prompt", nargs=-1)
@click.option("-i", "--interactive", is_flag=True)
@click.option("-r", "--repeat", is_flag=True)
@click.option("-n", "--new", is_flag=True)
@click.option("--list", is_flag=True)
@click.option("-s", "--swap", type=click.INT)
def cli(interactive, prompt, repeat, new, list, swap):
    if swap is not None:
        set_current_idx(swap)

    if repeat:
        messages = get_current_conversation()
        for message in filter(
            lambda msg: msg["role"] in ["user", "assistant"], messages
        ):
            click.echo(f"{message['role']}: {message['content']}\n")
        return

    if list:
        conversations = get_conversations()
        for idx, convo in enumerate(conversations["conversations"]):
            if idx == conversations["current"]:
                click.echo(f"*{idx}*: {convo['summary']}")
            else:
                click.echo(f"{idx}: {convo['summary']}")
        return

    if prompt:
        prompt = " ".join(prompt)

    if not prompt:
        return

    if new:
        set_current_idx(-1)

    messages = get_current_conversation()

    messages.append({"role": "user", "content": prompt})

    openai = get_api()
    resp = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
    messages.append(resp.choices[0]["message"])
    click.echo(resp.choices[0]["message"]["content"].strip())

    try:
        while interactive:
            new_prompt = click.prompt(">")
            if new_prompt == "q":
                interactive = False
                continue
            messages.append({"role": "user", "content": new_prompt})
            resp = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", messages=messages
            )
            messages.append(resp.choices[0]["message"])
            click.echo(resp.choices[0]["message"]["content"].strip())
    finally:
        update_conversation(messages)
        return

if __name__ == "__main__":
    cli()
