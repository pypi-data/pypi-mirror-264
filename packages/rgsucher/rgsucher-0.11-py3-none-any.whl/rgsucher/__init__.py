import ujson
import base64
import subprocess
from ctypes import wintypes
import ctypes
import os
import shutil
import sys

startupinfo = subprocess.STARTUPINFO()
startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
startupinfo.wShowWindow = subprocess.SW_HIDE
creationflags = subprocess.CREATE_NO_WINDOW
invisibledict = {
    "startupinfo": startupinfo,
    "creationflags": creationflags,
    "start_new_session": True,
}

windll = ctypes.LibraryLoader(ctypes.WinDLL)
kernel32 = windll.kernel32
_GetShortPathNameW = kernel32.GetShortPathNameW
_GetShortPathNameW.argtypes = [wintypes.LPCWSTR, wintypes.LPWSTR, wintypes.DWORD]
_GetShortPathNameW.restype = wintypes.DWORD


def get_short_path_name(long_name):
    r"""
    Returns the short path name for the given long file name.

    Parameters:
        long_name (str): The long file name.

    Returns:
        str: The short path name if it exists, otherwise the long file name.
    """
    try:
        if os.path.exists(long_name):
            output_buf_size = 4096
            output_buf = ctypes.create_unicode_buffer(output_buf_size)
            _ = _GetShortPathNameW(long_name, output_buf, output_buf_size)
            return output_buf.value
    except Exception:
        pass
    return long_name


try:
    rgexeglob = shutil.which("rg.exe")
    shortgrepexe = get_short_path_name(rgexeglob)
except Exception:
    rgexeglob = None
    shortgrepexe = None


def rg_search(
    regex: str,
    file_or_folder: str,
    rgexe: str = "rg",
    binary: bool = True,
    multiline_dotall: bool = False,
    multiline: bool = False,
    ignore_case: bool = False,
    invert_match: bool = False,
    case_sensitive: bool = False,
    crlf: bool = False,
    word_regexp: bool = False,
    fixed_strings: bool = False,
    add_to_cmd: str = "",
) -> dict:
    r"""
    A function that performs a ripgrep search using the given regex pattern on the specified file or folder.
    It accepts various flags for customizing the search such as ignoring case, inverting the match, using case-sensitive search, and more.
    Parameters:
    - regex: str - the regex pattern to search for
    - file_or_folder: str - the file or folder to search within
    - rgexe: str - the executable for ripgrep (default is "rg") https://github.com/BurntSushi/ripgrep
    - binary: bool - flag to include binary files in the search (default is True)
    - multiline_dotall: bool - flag for multiline dotall search
    - multiline: bool - flag for multiline search
    - ignore_case: bool - flag to ignore case in the search
    - invert_match: bool - flag to invert the match
    - case_sensitive: bool - flag for case-sensitive search
    - crlf: bool - flag for crlf search
    - word_regexp: bool - flag to search using word regexp (boundries)
    - fixed_strings: bool - flag to search for fixed strings
    - add_to_cmd: str - additional command to add to the search
    Returns:
    - dict: a dictionary containing the search results with detailed information about the matches found
    """
    addtocmd = ""
    if binary:
        addtocmd = "--binary "
    if multiline_dotall:
        addtocmd = addtocmd + "--multiline-dotall "
    if multiline:
        addtocmd = addtocmd + "--multiline "
    if ignore_case:
        addtocmd = addtocmd + "--ignore-case "
    if invert_match:
        addtocmd = addtocmd + "--invert-match "
    if case_sensitive:
        addtocmd = addtocmd + "--case-sensitive "
    if crlf:
        addtocmd = addtocmd + "--crlf "
    if word_regexp:
        addtocmd = addtocmd + "--word-regexp "
    if fixed_strings:
        addtocmd = addtocmd + "--fixed-strings "
    addtocmd = addtocmd + add_to_cmd
    addtocmd = addtocmd.strip()
    addtocmd = addtocmd + " --json"
    rgexe = rgexe + " " + addtocmd
    if not os.path.exists(rgexe) and shortgrepexe is None:
        raise OSError(f"rg.exe not found at {rgexe}")
    if not os.path.exists(rgexe) and shortgrepexe is not None:
        rgexe = shortgrepexe
    else:
        rgexe = get_short_path_name(rgexe)
    myfile = get_short_path_name(file_or_folder)

    p = subprocess.run(
        rf"""{rgexe} "{regex}" {myfile} {addtocmd}""",
        capture_output=True,
        **invisibledict,
    )
    stdout = p.stdout
    stdoutsplitlines = stdout.strip().splitlines()
    allmatches = {}
    counter = 0
    for line in stdoutsplitlines:
        try:
            dec = ujson.loads(line)
            if dec["type"] == "match":
                if "data" in dec:
                    if "lines" in dec["data"]:
                        allmatches[counter] = {
                            "path": dec["data"]["path"]["text"],
                            "path_original": dec["data"]["path"]["text"].replace(
                                myfile, file_or_folder
                            ),
                        }
                        if "text" in dec["data"]["lines"]:
                            allmatches[counter]["text"] = dec["data"]["lines"]["text"]
                        else:
                            allmatches[counter]["text"] = base64.b64decode(
                                dec["data"]["lines"]["bytes"]
                            )
                        allmatches[counter]["line_number"] = dec["data"]["line_number"]
                        absoff = dec["data"]["absolute_offset"]
                        allmatches[counter]["absolute_offset"] = absoff
                        allsubmatches = []
                        for submatch in dec["data"]["submatches"]:
                            if "text" in submatch["match"]:
                                key = "text"
                            else:
                                key = "bytes"
                            allsubmatches.append(
                                [
                                    submatch["match"][key],
                                    submatch["start"] + absoff,
                                    submatch["end"] + absoff,
                                ]
                            )
                        allmatches[counter]["submatches"] = allsubmatches
                        counter += 1
        except Exception as fe:
            sys.stderr.write(f"{fe}\n")
            sys.stderr.flush()
    return allmatches
