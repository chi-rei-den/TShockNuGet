import urllib.request
import json
import zipfile
import os
import shutil
import re
import datetime
from xml.sax.saxutils import escape

urllib.request.urlretrieve("https://api.github.com/repos/Pryaxis/TShock/releases", "gh.json")
lj = json.loads(open("gh.json", encoding="utf-8").read())
url = lj[0]["assets"][0]["browser_download_url"]
urllib.request.urlretrieve(url, "tshock.zip")
with zipfile.ZipFile("tshock.zip", "r") as zip_ref:
    zip_ref.extractall("target")

os.mkdir("binary")
excludes = ["Newtonsoft.Json.dll", "MySql.Data.dll", "BCrypt.Net.dll", "sqlite3.dll"]

for subdir, dirs, files in os.walk("target"):
    for file in files:
        filepath = subdir + os.sep + file

        if filepath.endswith(".exe") or filepath.endswith(".dll"):
            if file not in excludes:
                shutil.copy(filepath, "binary" + os.sep + file)

# (?P<xx>) is python style named group capture
ver = re.match("(?:v)?(?P<version>(?P<major>\d+)(\.(?P<minor>\d+))?(\.(?P<patch>\d+))?)(?P<suffix>-.*)?", lj[0]["tag_name"])
timepub = datetime.date.strftime(datetime.datetime.strptime(lj[0]["published_at"], "%Y-%m-%dT%H:%M:%SZ"), "%Y%m%d")
verstr = f"{ver.group('major')}.{ver.group('minor') or 0}.{ver.group('patch') or 0}"
if len(ver.group('suffix') or '') > 0:
    verstr += f".{timepub}{ver.group('suffix') or ''}"

nuspec = open("template.nuspec", encoding="utf-8").read()\
             .replace("IDPLACEHOLDER", "TerrariaServer.TShock")\
             .replace("VERSIONPLACEHOLDER", verstr)\
             .replace("NAMEPLACEHOLDER", escape(lj[0]["name"] + "\r\n\r\n" + lj[0]["body"]))

with open("tshock.nuspec", "w", encoding="utf-8") as f:
    f.write(nuspec)

print("Tag: " + lj[0]["tag_name"])
print("Name: " + lj[0]["name"])
print("Body: " + lj[0]["body"])