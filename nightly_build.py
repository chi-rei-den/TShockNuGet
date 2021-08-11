import os
import shutil
import datetime
import subprocess
from xml.sax.saxutils import escape

os.mkdir("binary")
excludes = ["Newtonsoft.Json.dll", "MySql.Data.dll", "BCrypt.Net.dll", "sqlite3.dll"]

for subdir, dirs, files in os.walk("../TShock/TShockAPI/bin/Debug"):
    for file in files:
        filepath = subdir + os.sep + file

        if filepath.endswith(".exe") or filepath.endswith(".dll"):
            if file not in excludes:
                shutil.copy(filepath, "binary" + os.sep + file)
                print(filepath)

authortime = int(subprocess.check_output(["git", "log", "HEAD~1", "-1", "--format=%at"], cwd="../TShock/"))
authortime = datetime.datetime.utcfromtimestamp(authortime).strftime("%Y.%m")
revcount = int(subprocess.check_output(["git", "rev-list", "--count", "HEAD~1"], cwd="../TShock/"))
packageversion = f"{authortime}.{revcount}"
releasenote = subprocess.check_output(["git", "log", "HEAD~1", "-1", "--format=medium"], cwd="../TShock/").decode("utf-8")
nuspec = open("template.nuspec", encoding="utf-8").read()\
             .replace("IDPLACEHOLDER", "TerrariaServer.TShock.Nightly")\
             .replace("VERSIONPLACEHOLDER", packageversion)\
             .replace("NAMEPLACEHOLDER", escape(releasenote))

with open("tshock.nuspec", "w") as f:
    f.write(nuspec)

print("Author time: " + str(authortime))
print("Version: " + packageversion)
print("Release Notes: " + releasenote)