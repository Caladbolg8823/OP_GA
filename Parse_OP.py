import re


def getData(fileName):
    f = open(fileName, "r")
    content = f.read()
    coords = re.findall(r"(\d+.*d*)\t(\d+.*d*)\t(\d+)",
                        content, re.MULTILINE)

    max_time = re.findall(r"(\d+)\t(\d+)", content)
    max_time = list(max_time[-1])
    max_time = int(max_time[0])

    coords = [(float(a), float(b), int(c)) for a, b, c in coords]
    x_data = [(v[0]) for i, v in enumerate(coords)]
    y_data = [(v[1]) for i, v in enumerate(coords)]
    benfit = [(v[2]) for i, v in enumerate(coords)]

    XY = zip(x_data, y_data)
    coords = list(XY)

    return coords, benfit, max_time
