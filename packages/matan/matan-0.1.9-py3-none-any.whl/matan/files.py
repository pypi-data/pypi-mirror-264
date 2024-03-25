import glob, os
import re

__all__ = ["files", "manager"]


class manager:
    def __init__(self):
        """This class can manage the files as well as it's parameters

        This class helps managing he files, find their names/paths, extract the method of manufacturing or other
        parameters

        """

    def find(self, path, extension: str):
        """Method to search for the result files

        This method allows you to find the files in given path, and returns their result objects.

        Parameters
        ----------
        path : str
            This variable is used to put path to your files
        extension : str
            Extension is the extention of your files. If your file is .csv put csv in there, be aware and do not put the dot before your extension

        Examples
        --------
        FIXME: Add docs.

        """
        if extension.startswith("."):
            extension = extension[1:]

        self.files = glob.glob(os.path.join(path, f"*.{extension}"))
        self.results = [result(path) for path in self.files]


class result:
    def __init__(self, path, *args, **kwargs):
        """this class is for managing single result file

        using this class you can extract information like name, modifications, comments, composition etc. It is possible to extract such information from filename.
        Unfortunately now you need to use strict filename format:
        ```
        MMETHOD-IIpMATERIAL-IIpMATERIAL[comment].extension
        ```

        - first letter is the first letter of your modification list, if the list is empty, then it is omitted,

        - Next letters before "-" sign describing manufacturing method of this result.

        - Next letters after "-" sign are compounds, so first II signs describes percents of the MATERIAL compound, and they are divided by "p" sign.

        - Comments needs to be closed in square brackets. You can play with this class by files module functions given below.

        Parameters
        ----------
        path : str
            This variable is used to put path to your files

        Examples
        --------
        FIXME: Add docs.
        """
        self.path = path
        self.name, self.extension = os.path.splitext(os.path.split(path)[1])
        self.name, self.number = find_number(self.name, *args, **kwargs)
        self.comments, self.name = find_comments(self.name)
        if "modifications" in kwargs:
            self.modification = find_modification(self.name, *args, **kwargs)
            if self.modification is not None:
                self.name = self.name[1:]
        self.method = find_method(self.name, **kwargs)
        self.composition = find_composition(self.name, *args, **kwargs)


def find_method(name: str, delimiter: str = "-", placement: int = 0, *args, **kwargs):
    """Find the technique how the material was created

    Find the method how the material was created, what methods were used to modify it, etc. To do so it is using
    first letters of filename, so for extruded parts you can use EXT, for annealed extruded parts you can use aEXT
    etc.

    Parameters
    ----------
    path : str
        path for your file
    delimiter : str
        what sign you wanna use to finish your method string. By default it is -

    Examples
    --------
    FIXME: Add docs.

    """
    return name.split(delimiter)[placement]


@staticmethod
def find_modification(
    name: str, modifications: list, place: int = 0, *args, **kwargs
) -> str:
    """function to extract the modification from the filename

    Parameters
    ----------
    name : str
        name of the sample
    modifications : list
        list of possible modification
    place : int
        placement of the first letter of each possible modification


    Returns
    -------
    Modification name

    Raises
    ------
    ValueError
        when no modification list is given

    Examples
    --------
    FIXME: Add docs.


    """

    if not isinstance(modifications, list):
        raise ValueError("Put list of modifications!")
    for mod in modifications:
        letter = mod[place]
        if name[place] == letter:
            return mod
        else:
            continue
    return None


@staticmethod
def find_composition(
    name: str, delimiter: str = "-", percent_sign="p", *args, **kwargs
) -> dict:
    """method to obtain material ingridiens from name, as I usually name files extracted from machine with code allowing me to get that information from filename

    Parameters
    ----------
    name : str
        filename to process
    delimiter : str
       delimiter for the composition, default "-"
    percent_sign :
       `percent_sign` sign, default "p"

    Returns
    -------
    dict
        dict of the composition

    Examples
    --------
       >>> import matan as mt
       >>> name = "AFDM-10pPET-90pPC_1.csv"
       >>> composition = mt.files.find_composition(name,modifications=["Annealing", "Test"])
       >>> composition
       output: {PET: 10, PC:90}

    """
    splitted = name.split(delimiter)
    comp = {}
    for name in splitted[1:]:
        comp.update(_extract_info(name, percent_sign))
    return comp


def find_comments(name):
    """function to find the comments in the filename

    extract everything in square brackets (hardcoded for now),

    Parameters
    ----------
    name : str
        filename


    Returns
    --------
    returns tuple of (comments, cleaned_text)
        `cleaned_text` is the filename without comment

    Examples
    --------
    FIXME: Add docs.
    """
    pattern = (
        r"\[.*?\]"  # a regular expression pattern to match text between square brackets
    )
    matches = re.findall(pattern, name)  # find all matches of the pattern in the string
    comments = "".join(matches)  # concatenate all the matches into a single string
    cleaned_text = re.sub(
        pattern, "", name
    )  # remove all the matches from the original string
    comments = re.sub(
        r"[\[\]]", "", comments
    )  # remove square brackets from the removed text
    return comments, cleaned_text


def find_number(name, number_delimiter="_", *args, **kwargs):
    """function to find number of the test

    Parameters
    ----------
    name : str
        filename of the samole
    number_delimiter : str
        delimiter for the number

    Examples
    --------
    FIXME: Add docs.


    """
    number = name.split("_")
    name = number[0]
    number = number[len(number) - 1]
    return name, number


def _extract_info(s, delimiter="p"):
    pattern = rf"(\d+){delimiter}(.+)"
    match = re.match(pattern, s)
    result = {}
    if match:
        result[match.group(2)] = [int(match.group(1))]
    # else:
    #     return None
    return result
