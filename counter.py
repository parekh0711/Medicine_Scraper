from bs4 import BeautifulSoup
import requests

urls = [
    "https://www.1mg.com/drugs/azithral-500-tablet-325616",
    "https://www.1mg.com/drugs/ofstan-oz-200mg-500mg-tablet-521775",
]
fptr = open("input.txt", "r")
f1 = fptr.readlines()
for index, url in enumerate(f1):
    print("doing", index)
    r = requests.get(url.strip("\n"))
    soup = BeautifulSoup(r.text, "html.parser")
    fptr = open("trial.txt", "w", encoding="utf-8")
    # print(soup.prettify(), file=fptr)

    name = soup.find("h1", attrs={"class": "col-6"}).text

    temp = soup.findAll(
        "div",
        attrs={"class": "FactBox__rowContent__2YA1r FactBox__flexCenter__j9P_K col-3"},
    )
    manufacturer = temp[0].text
    salt = temp[1].text

    introduction = soup.find("div", attrs={"class": "marginTop-8 col-6"}).text

    price = soup.find(
        "div", attrs={"class": "Price__price__xOjt5 Price__align__2a2LF"}
    ).text

    uses = soup.find("ul", attrs={"class": "marginTop-8"}).text

    temp = soup.find("div", attrs={"id": "side_effects_0"},)
    temp = temp.find(
        "div",
        attrs={
            "class": "AccordionGroup__content__2gkNe AccordionGroup__collapsed__2X2Ki"
        },
    )
    temp = temp.find("div", attrs={"class": "container-fluid-padded"})
    temp = temp.findAll("li")
    side_effects = [t.text for t in temp]
    coping = [side_effects[i] for i in range(len(side_effects) // 2, len(side_effects))]
    side_effects = side_effects[: len(side_effects) // 2]
    temp = soup.find(
        "div",
        attrs={
            "class": "marginTop-16 Accordion__content__3S9jw Accordion__contentCollapsed__3C0AR"
        },
    )
    temp = temp.findAll("div", attrs={"class": "marginBoth-8"})
    for index, t in enumerate(temp):
        t2 = t.text.replace(coping[index], "")
        coping[index] += ":"
        coping[index] += t2

    temp = soup.find("div", attrs={"id": "how_to_take_0"})
    how_to_use = temp.find("p", attrs={"class": "col-6"}).text

    temp = soup.find("div", attrs={"id": "how_it_works_0"})
    how_it_works = temp.find("p", attrs={"class": "col-6"}).text

    temp = soup.find("div", attrs={"id": "warnings"})
    headings = temp.findAll("div", attrs={"class": "Accordion__title__2SQGe"})
    headings = [h.text for h in headings]
    shorts = temp.findAll("div", attrs={"class": "DrugContainer__container__2ZFXt"})
    shorts = [s.text for s in shorts]
    longs = temp.findAll("p", attrs={"class": "marginTop-8 bodyRegular"})
    longs = [l.text for l in longs]

    forget = soup.find("p", attrs={"class": "marginTop-8"}).text

    temp = soup.find("div", attrs={"id": "alternate_brands"})
    temp2 = temp.findAll(
        "div", attrs={"class": "DrugContainer__rowContent__374pc col-3"}
    )
    new = ""
    alternates = []
    for index, a in enumerate(temp2):
        if index % 2 == 0:
            new += a.find("a").text
            new += ":"
            new += a.find("span").text
        else:
            new += ":"
            new += a.find("span").text
            alternates.append(new)
            new = ""

    print(
        name,
        manufacturer,
        salt,
        introduction,
        price,
        uses,
        side_effects,
        coping,
        how_to_use,
        how_it_works,
        headings,
        shorts,
        longs,
        forget,
        alternates,
        "\n",
        sep="\n",
        file=open("checker.txt", "a+", encoding="utf-8"),
    )
