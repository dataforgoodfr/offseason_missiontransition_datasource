import re


def get_clean_text(
        input_text: str,
        debug_print: bool
) -> str:

    text = remove_special_characters(
        text=input_text,
        debug_print=debug_print
    )

    return text


def remove_special_characters(
        text: str,
        debug_print: bool
) -> str:

    special_characters_to_remove = [
        '', '', '', '', '', '►', '', '', '', '©',
        '☐', '', '', '', '', '', '', '', '', '➢',
        '✓', '■', '', ''
    ]

    for c in special_characters_to_remove:
        text = text.replace(c, "")

    if debug_print:

        character_list = set(text)
        for character in character_list:
            if re.match(
                    r"^[a-zA-Z0-9'\-()’àçô–è.€Ééê/»«:\[;=*,\]@%û<>ù&+!?]&*$",
                    character
            ) is None:
                print(character)

    return text
