from pathlib import Path
import yaml

params = {"censyssecret": ["censys", "secret"], "circlusername":["circl", "username"], "circlpassword":["circl", "password"], "digicertusername": ["certcentral", "username"], "facebooksecret":["facebook", "secret"], "fofausername": ["fofa", "username"], "rikiqusername":["passivetotal", "username"], "spamhaususername":["spamhaus", "username"], "spamhauspassword":["spamhaus", "password"], "twittersecret":["twitter", "secret"], "zoomeyeusername":["zoomeye", "username"], "zoomeyepassword":["zoomeye", "password"], "yandexusername":["yandex", "username"]}

def ReconConfig(name, key=None, get=None):
    name = name.replace("_", "").lower()

    names = {
        "shodan":"SHODAN_API_KEY",
        "whoisxml":"WHOISXML_API",
        "xssserver":"XSS_SERVER",
        "collabserver":"COLLAB_SERVER",
        "slackchanel":"slack_channel",
        "slackauth":"slack_auth",
    }


    if name in names:
        name = names[name]
        file = "../reconftw.cfg"

        lines = open(file, "r").readlines()

        if key != None:
            subs = {}

            for line in lines:
                if name in line:
                    if key != "":
                        subs[line] = f'{name}="{key}' + '"\n'

                    else:
                        subs[line] = f'#{name}' + '="XXXXXXXXXXXXX"\n'
                    break
            for sub, value in subs.items():
                replace = Path(file)
                replace.write_text(replace.read_text().replace(sub, value, 1))

        elif get == True:
            result = next(
                (
                    line.split("=")[1].replace(" ", "")
                    for line in lines
                    if name in line
                ),
                "",
            )
            if "XXXXXXXX" in result or "XXX-XXX-XXX" in result:
                return ""
            else:
                return result.replace('"', '')


#https://ddaniboy.github.io/sariel.html
def amassConfig(name, key=None, get=None):
    file = f"{str(Path.home())}/.config/amass/config.ini"
    name = name.lower()

    lines = open(file, "r").readlines()

    if name in params:
        param = params[name][1]
        name = params[name][0]
    else:
        param = "apikey"


    conf = []
    cont = False

    sub = ""
    apikey = ""

    for line in lines:

        if f"data_sources.{name}" in line.lower():
            cont = True

        if cont == True:
            conf.append(line)
            sub += line
            if param in line:
                cont = False

                if len(line.split("=")) > 1:
                    apikey = line.split("=")[1].replace("\n", "")
                else:
                    apikey = ""
                break



    if get == True:
        return apikey.replace(" ", "")
    apikey = apikey.replace(" ", "")
    key = key.replace(" ", "")
    if apikey != key != "":
        final = ""
        for con in conf:
            if con != "":
                if con[0] == "#":
                    con = con.replace("#", "", 1)
                while con[0] == " ":
                    con = con.replace(" ", "", 1)

            if param in con.lower():
                con = f"{param} = {key}" + "\n"


            final += con

        replace = Path(file)
        replace.write_text(replace.read_text().replace(sub, final, 1))



    elif apikey != "" and key == "":
        final = ""
        for con in conf:
            if con != "":
                con = f"#{con}"
            if param in con.lower():
                con = f"#{param}" + " =\n"


            final += con


        replace = Path(file)
        replace.write_text(replace.read_text().replace(sub, final, 1))




def GithubConfig(number, key=None, get=None):
    file = f"{str(Path.home())}/Tools/.github_tokens"
    number = int(number)-1
    lines = open(file, "r").readlines()

    if len(lines) <= 5:

        with open(file, "w") as lines:
            for _ in range(0, 6):
                lines.write("\n")
    if key != None:
        if key != "":
            lines[number] = key+"\n"
        elif lines[number] != key:
            lines[number] = "\n"

        with open(file, "w") as gitTokens:
            for item in lines:
                gitTokens.write(item)
    if get == True:

        lines = open(file, "r").readlines()

        return lines[number]
           
def theHarvesterConfig(name, key=None, get=None):
    namefile = f"{str(Path.home())}/Tools/theHarvester/api-keys.yaml"
    listOfNames = {"chaos":"projectDiscovery"}

    if name.lower() in listOfNames:
        name = listOfNames[name.lower()]

    var = "secret" if name == "censys" else "key"
    with open(namefile) as file:
        if key != None:
            data = yaml.load(file, Loader=yaml.FullLoader)

            if key not in [data["apikeys"][name][var], ""]:
                data["apikeys"][name][var] = key

            elif key == "" and data["apikeys"][name][var] != None:
                data["apikeys"][name][var] = None


            with open(namefile, "w") as comp:
                yaml.dump(data, comp)

        elif get == True:
            data = yaml.load(file, Loader=yaml.FullLoader)

            result = data["apikeys"][name][var]

            return '' if result is None else result

def h8mailConfig(name, key=None, get=None):
    file = f"{str(Path.home())}/Tools/h8mail_config.ini"

    lines = open(file, "r").readlines()
    sub=""

    if key != None:
        for line in lines:
            line = line.replace("\n", "")
            if name in line and key != "":
                sub = line

                very = line.split("=")[1].replace(" ", "")

                if key != very:
                    while line[0] == ";":
                        line = line.replace(";", "", 1)

                    while line[0] == " ":
                        line = line.replace(" ", "", 1)


                    final = line.split("=")[0]+"= "+key
                    replace = Path(file)
                    replace.write_text(replace.read_text().replace(sub, final, 1))
                    break

            elif name in line:
                final = f";{name} = "
                sub = line


                replace = Path(file)
                replace.write_text(replace.read_text().replace(sub, final, 1))
                break
    elif get == True:
        key = ""
        for line in lines:

            line = line.replace("\n", "")
            if name in line:
                sub = line

                key = line.split("=")[1].replace(" ", "")

                break

        return key