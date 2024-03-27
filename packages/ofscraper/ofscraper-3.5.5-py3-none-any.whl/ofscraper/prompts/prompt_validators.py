import json
import pathlib
import platform
import re
import string
import textwrap

import arrow
from pathvalidate import validate_filename, validate_filepath
from prompt_toolkit.validation import Validator

import ofscraper.classes.placeholder as placeholders
import ofscraper.utils.paths as paths
import ofscraper.utils.profiles as profiles


class MultiValidator(Validator):
    """:Runs Multiple Validators Since Inquirerpy does seem to support this functionality natively

    Args:
        *args:List of validator objects

    """

    def __init__(self, *args):
        self.inputs = args

    def validate(self, document) -> None:
        for input in self.inputs:
            try:
                if isinstance(input, Validator):
                    input.validate(document)
                else:
                    if input(document.text) == False:
                        raise Exception()
            except Exception as E:
                raise E


def currentProfilesValidator():
    def callable(x):
        x = profiles.profile_name_fixer(x)
        return x not in set(profiles.get_profile_names())

    return Validator.from_callable(
        callable, "You can not change name to a current profile name"
    )


def currentProfilesCreationValidator():
    def callable(x):
        x = profiles.profile_name_fixer(x)
        return x not in set(profiles.get_profile_names())

    return Validator.from_callable(callable, "This Profile already exists")


def currentProfileDeleteValidator():
    def callable(x):
        return profiles.profile_name_fixer(x) != profiles.get_active_profile()

    return Validator.from_callable(callable, "You can not delete the active profile")


def emptyListValidator():
    def callable(x):
        return len(x) > 0

    return Validator.from_callable(callable, "You must select at least one")


def cleanTextInput(x):
    return x.strip()


def jsonValidator():
    def callable(x):
        try:
            json.loads(x)
            return True
        except:
            return False

    return Validator.from_callable(
        callable,
        "Invalid JSON syntax",
        move_cursor_to_end=True,
    )


def jsonloader(x):
    try:
        return json.loads(x)
    except TypeError:
        return None
    except json.JSONDecodeError:
        return None
    except Exception as E:
        raise E


def namevalitator():
    def callable(x):
        validchars = re.search("[a-zA-Z0-9_]*", x)
        return validchars != None and len(x) == len(validchars.group(0))

    return Validator.from_callable(
        callable,
        "ONLY letters, numbers, and underscores are allowed",
        move_cursor_to_end=True,
    )


def dirformatvalidator():
    def callable(x):
        try:
            testplaceholders = list(
                filter(lambda x: x != None, [v[1] for v in string.Formatter().parse(x)])
            )
            validplaceholders = placeholders.all_placeholders()
            if (
                len(
                    list(
                        filter(
                            lambda x: x not in validplaceholders
                            or not x.find("custom"),
                            testplaceholders,
                        )
                    )
                )
                > 0
            ):
                return False
            result = {}

            for d in list(map(lambda x: {x: "placeholder"}, placeholders)):
                result.update(d)
            validate_filepath(
                str(pathlib.Path(x.format(**result))), platform=platform.system()
            )

            return True
        except:
            return False

    return Validator.from_callable(
        callable,
        textwrap.dedent(
            f"""
Improper syntax or invalid placeholder
"""
        ).strip(),
        move_cursor_to_end=True,
    )


def fileformatvalidator():
    def callable(x):
        try:
            placeholders = list(
                filter(lambda x: x != None, [v[1] for v in string.Formatter().parse(x)])
            )
            validplaceholders = set(
                [
                    "date",
                    "responsetype",
                    "mediatype",
                    "model_id",
                    "first_letter",
                    "sitename",
                    "model_username",
                    "post_id",
                    "filename",
                    "value",
                    "text",
                    "ext",
                ]
            )

            if (
                len(list(filter(lambda x: x not in validplaceholders, placeholders)))
                > 0
            ):
                return False
            result = {}

            for d in list(map(lambda x: {x: "placeholder"}, placeholders)):
                result.update(d)
            validate_filename(x.format(**result), platform=platform.system())

            return True
        except:
            return False

    return Validator.from_callable(
        callable,
        textwrap.dedent(
            f"""
Improper syntax or invalid placeholder
"""
        ).strip(),
        move_cursor_to_end=True,
    )


def dateplaceholdervalidator():
    def callable(x):
        try:
            if arrow.utcnow().format(x) == x:
                return False
            return True
        except:
            return False

    return Validator.from_callable(
        callable,
        """
    Date Format is invalid -> https://arrow.readthedocs.io/en/latest/guide.html#supported-tokens
                """,
        True,
    )


def mp4decryptpathvalidator():
    def callable(x):
        return paths.mp4decryptpathcheck(x)

    return Validator.from_callable(
        callable,
        textwrap.dedent(
            f"""
Path to mp4decrypt is not valid filepath or does not exists
"""
        ).strip(),
        move_cursor_to_end=True,
    )


def mp4decryptexecutevalidator():
    def callable(x):
        return paths.mp4decryptexecutecheck(x)

    return Validator.from_callable(
        callable,
        textwrap.dedent(
            f"""
Path is valid but the given path could not be verified to be mp4decrypt
"""
        ).strip(),
        move_cursor_to_end=True,
    )


def ffmpegpathvalidator():
    def callable(x):
        return paths.ffmpegpathcheck(x)

    return Validator.from_callable(
        callable,
        textwrap.dedent(
            f"""
Path to ffmpeg is not valid filepath or does not exists
"""
        ).strip(),
        move_cursor_to_end=True,
    )


def ffmpegexecutevalidator():
    def callable(x):
        return paths.ffmpegexecutecheck(x)

    return Validator.from_callable(
        callable,
        textwrap.dedent(
            f"""
Path is valid but the given path could not be verified to be ffmpeg
"""
        ).strip(),
        move_cursor_to_end=True,
    )


def metadatavalidator():
    def callable(x):
        try:
            placeholders = list(
                filter(lambda x: x != None, [v[1] for v in string.Formatter().parse(x)])
            )
            validplaceholders = set(
                [
                    "sitename",
                    "first_letter",
                    "model_username",
                    "model_id",
                    "configpath",
                    "profile",
                ]
            )
            if (
                len(list(filter(lambda x: x not in validplaceholders, placeholders)))
                > 0
            ):
                return False
            result = {}

            for d in list(map(lambda x: {x: "placeholder"}, placeholders)):
                result.update(d)
            validate_filepath(
                str(pathlib.Path(x.format(**result))), platform=platform.system()
            )

            return True
        except:
            return False

    return Validator.from_callable(
        callable,
        textwrap.dedent(
            f"""
Improper syntax or invalid placeholder
"""
        ).strip(),
        move_cursor_to_end=True,
    )


def DiscordValidator():
    def callable(x):
        if len(x) == 0:
            return True
        return re.search("https://discord.com/api/webhooks/[0-9]*/[0-9a-z]*", x) != None

    return Validator.from_callable(
        callable,
        textwrap.dedent(
            """
must be discord webhook -> example: https://discord.com/api/webhooks/{numeric}/{alphanumeric}
    """
        ).strip(),
    )
