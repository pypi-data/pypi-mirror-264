def save_text(text: str, f: str) -> None:
    with open(f, "w") as fp:
        fp.write(text)
