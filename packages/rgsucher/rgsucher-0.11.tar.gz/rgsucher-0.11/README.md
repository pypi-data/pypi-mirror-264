# ripgrep search

### Tested against Windows / Python 3.11 / Anaconda

### pip install rgsucher

```PY
from rgsucher import rg_search
import numpy as np

# searching in a folder
wholeregex = r"\d+"
imagefile = r"C:\Users\hansc\Documents\fubax\Disable-IPv6\common"  # folder
server_ip = rg_search(
    regex=wholeregex,
    file_or_folder=imagefile,
    rgexe=r"C:\ProgramData\chocolatey\bin\rg.exe",
    binary=True,
    multiline_dotall=False,
    multiline=False,
    ignore_case=False,
    invert_match=False,
    case_sensitive=False,
    crlf=False,
    word_regexp=False,
    fixed_strings=False,
)

# searching in a file
allregex = [
    r"""\s*<string name=\"server_ip\">\d{3}.\d{3}.\d{3}.\d{3}</string>""",
    r"""\s*<string name=\"Defaultserver\">\d{3}.\d{3}.\d{3}.\d{3}</string>""",
    r"""\s*<string name=\"server_port\">\d{5}</string>""",
    r"""\s*<int name=\"Defaultport\" value=\"\d{5}\" />""",
]
wholeregex = r"(?:(?:" + ")|(?:".join(allregex) + "))"
imagefile = r"C:\ProgramData\BlueStacks_nxt\Engine\Rvc64_42\Data.vhdx"  #file
server_ip = rg_search(
    regex=wholeregex,
    file_or_folder=imagefile,
    rgexe=r"C:\ProgramData\chocolatey\bin\rg.exe",
    binary=True,
    multiline_dotall=False,
    multiline=False,
    ignore_case=False,
    invert_match=False,
    case_sensitive=False,
    crlf=False,
    word_regexp=False,
    fixed_strings=False,
    add_to_cmd="",
)

# replacing the matches using numpy
import re

print(server_ip)
myip = "112.112.131.121"
myport = "55164"
with open(imagefile, "rb") as f:
    imagedata = f.read()
nparray = np.frombuffer(imagedata, dtype=np.uint8).copy()

for k, v in server_ip.items():
    for submatch in v["submatches"]:
        print(submatch)
        original = submatch[0]
        new = re.sub(r">\d{3}.\d{3}.\d{3}.\d{3}<", rf">{myip}<", original)
        new = re.sub(r">\d{4,5}<", rf">{myport}<", new)
        if len(new) > len(original):
            new = new[1:]
        new = re.sub(r'"\d{4,5}"', rf'"{myport}"', new)
        if len(new) > len(original):
            new = new[1:]
        print(new, original)

        replacem = new.encode()
        replacemint = list(replacem)
        coun = 0
        for i in range(submatch[1], submatch[2]):
            nparray[i] = replacemint[coun]
            coun += 1
with open(imagefile, "wb") as f:
    f.write(nparray.tobytes())
```