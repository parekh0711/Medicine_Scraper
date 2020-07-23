from bs4 import BeautifulSoup
import requests
import urllib.request
import re

input_file_name = "input.txt"
# f1 = [
#     "https://www.1mg.com/drugs/azithral-500-tablet-325616",
#     "https://www.1mg.com/drugs/ofstan-oz-200mg-500mg-tablet-521775",
# ]
fptr = open(input_file_name, "r")
f1 = fptr.readlines()
for index, url in enumerate(f1):
    try:
        print("doing", index + 1)
        while 1:
            try:
                r = requests.get(url.strip("\n"))
                break
            except:
                "Bad net, trying again"
        soup = BeautifulSoup(r.text, "html.parser")
        fptr = open("trial.txt", "w", encoding="utf-8")
        # print(soup.prettify(), file=open("tester.html", "w", encoding="utf-8"))

        name = soup.find("h1", attrs={"class": "col-6"}).text

        if "Tablet" in name:
            type = "Tablet"
        elif "Syrup" in name:
            type = "Syrup"
        elif "Capsule" in name:
            type = "Capsule"
        elif "Injection" in name:
            type = "Injection"
        elif "Gel" in name:
            type = "Gel"
        else:
            type = "no type given"

        temp = soup.findAll(
            "div",
            attrs={
                "class": "FactBox__rowContent__2YA1r FactBox__flexCenter__j9P_K col-3"
            },
        )
        try:
            manufacturer = temp[1].text
        except:
            manufacturer = "not given"
        try:
            salt = temp[0].text
        except:
            salt = "not given"
        try:
            temp = temp[1]
            manufacturer_link = "www.1mg.com" + temp.find("a", href=True)["href"]
        except:
            manufacturer_link = "not given"

        try:
            size = soup.find(
                "span",
                attrs={
                    "class": "bodyRegular TransactionWidget__marginLeft__2_BGK TransactionWidget__flexGrow__2gouh"
                },
            ).text
        except:
            size = "No size given"

        try:
            introduction = soup.find("div", attrs={"class": "marginTop-8 col-6"}).text
        except:
            introduction = "not given"
        try:
            price = soup.find(
                "div", attrs={"class": "Price__price__xOjt5 Price__align__2a2LF"}
            ).text
        except:
            price = "not given"
        try:
            if "%" in price:
                discount = price[-11:]
                price = price.replace(discount, "")
                price = price.split("MRP")
                discounted_price = price[0]
                price = "MRP" + price[1]
            else:
                discounted_price = "no discount given"
                discount = "no discount given"
        except:
            price = soup.find(
                "div", attrs={"class": "Price__price__xOjt5 Price__align__2a2LF"}
            ).text

        try:
            uses = soup.find("ul", attrs={"class": "marginTop-8"}).findAll("li")
            uses = [u.text for u in uses]
            uses = "||".join(uses)
        except:
            try:
                uses = soup.find("ul", attrs={"class": "marginTop-8"}).text
            except:
                uses = "not given"

        try:
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
            coping = [
                side_effects[i]
                for i in range(len(side_effects) // 2, len(side_effects))
            ]
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
            side_effects = " AaAaAa ".join(side_effects)
            coping = " BbBbBb ".join(coping)
        except:
            side_effects = "not given"
            coping = "not given"
        try:
            temp = soup.find("div", attrs={"id": "how_to_take_0"})
            how_to_use = temp.find("p", attrs={"class": "col-6"}).text.replace(
                "<br>", ""
            )
            how_to_use = how_to_use.replace("\n", "")
        except:
            how_to_use = "not given"

        temp = soup.find("div", attrs={"id": "how_it_works_0"})
        try:
            how_it_works = temp.find("p", attrs={"class": "col-6"}).text.replace(
                "<br>", ""
            )
            how_it_works = how_it_works.replace("\n", "")
        except:
            how_it_works = "not given"

        try:
            temp = soup.find("div", attrs={"id": "warnings"})
            headings = temp.findAll("div", attrs={"class": "Accordion__title__2SQGe"})
            headings = [h.text for h in headings]
            shorts = temp.findAll(
                "div", attrs={"class": "DrugContainer__container__2ZFXt"}
            )
            shorts = [s.text for s in shorts]
            longs = temp.findAll("p", attrs={"class": "marginTop-8 bodyRegular"})
            longs = [l.text for l in longs]
            matrix = list(map(" || ".join, zip(headings, shorts, longs)))
            warnings = " CcCcCc ".join(matrix)
        except:
            warnings = "not given"

        try:
            forget = soup.find("p", attrs={"class": "marginTop-8"}).text
        except:
            forget = "not given"

        try:
            temp = soup.find("div", attrs={"id": "alternate_brands"})
            temp2 = temp.findAll("div", attrs={"class": "container-fluid-padded"})[1]
            alternates = url.replace("drugs/", "drugs-substitutes/")
        except:
            alternates = ""

        try:
            temp = soup.find("div", attrs={"id": "expert_advice_0"})
            quick_tips = "||".join([t.text for t in temp.findAll("li")])
        except:
            quick_tips = "no quick tips given"
        if not quick_tips:
            quick_tips = "no quick tips given"

        try:
            temp = soup.find("div", attrs={"id": "faq_0"})
            temp = temp.find(
                "div",
                attrs={
                    "class": "AccordionGroup__content__2gkNe AccordionGroup__collapsed__2X2Ki"
                },
            )
            faqs = temp.text.replace(".Q", ".||Q")
        except:
            faqs = "no faqs given"

        try:
            temp = soup.find("div", attrs={"id": "References"})
            references = " || ".join([t.text for t in temp.findAll("li") if t.text])
            references_links = " || ".join(
                [t["href"] for t in temp.findAll("a", href=True)]
            )
        except:
            references = "no references given"
            references_links = "no references given"

        try:
            temp = soup.findAll("div", attrs={"class": "marginBoth-16"})
            for t in temp:
                if t.findAll("p", attrs={"class": "bodySemiBold marginTop-16"}) != []:
                    temp = t
                    break
            feedback = ""
            for tag in t.find_all():
                if tag.name == "p" and tag["class"] == ["bodySemiBold", "marginTop-16"]:
                    feedback += " || " + tag.text + " | "
                elif tag.name == "span":
                    feedback += tag.text + " "
                    if feedback[-2] == "%":
                        feedback += "| "
        except:
            feedback = "No feedback given"

        try:
            temp = soup.find("div", attrs={"id": "Fact Box"})
            temp2 = [t.text for t in temp.findAll("div", attrs={"class": "col-4"})]
            temp = [t.text for t in temp.findAll("div", attrs={"class": "col-2"})]
            matrix = list(map(" || ".join, zip(temp, temp2)))
            fact_box = " DdDdDd ".join(matrix)
        except:
            fact_box = "no fact box given"

        temp = soup.find(
            "div",
            attrs={"class": "DrugContainer__content__18wg5 container-fluid-padded"},
        )
        try:
            address = ""
            address += temp.findAll("h3")[1].text + "||"
            address += temp.findAll("p", attrs={"class": "bodyRegular"})[1].text
        except:
            address = " no address given"
        if alternates:
            # alternates = alternates.strip("\n")
            # print(name + "," + alternates, file=open("alternates.txt", "a+"))
            entry = alternates.strip("\n")
            try:
                url = entry
                while 1:
                    try:
                        r = requests.get(url.strip("\n"))
                        break
                    except:
                        "Bad net, trying again"
                soup = BeautifulSoup(r.text, "html.parser")
                count = int(
                    soup.find("div", attrs={"class": "col-xs-5 text-small"}).text.strip(
                        "Alternate Brands",
                    )
                )
                if count <= 15:
                    # print("Count < 15")
                    alternates = []
                    temp = soup.findAll(
                        "div", attrs={"class": "container-fluid js-alert-section"}
                    )
                    temp = soup.findAll("li", attrs={"class": "list-item item"})
                    for e in temp:
                        brand_name = e.find("a").text
                        brand_link = "https://www.1mg.com" + e.find("a")["href"]
                        brand_manufacturer = e.find(
                            "span", attrs={"class": "item-manufacturer"}
                        ).text
                        brand_price = e.find("div", attrs={"class": "item-price"}).text
                        brand_discount = e.find(
                            "div", attrs={"class": "item-save"}
                        ).text
                        alternates.append(
                            "||".join(
                                [
                                    brand_name,
                                    brand_link,
                                    brand_manufacturer,
                                    brand_price,
                                    brand_discount,
                                ]
                            )
                        )
                    raise KeyboardInterrupt
                link = (
                    soup.find(
                        "a",
                        attrs={
                            "class": "pgntnCntnrBar btn btn-primary text-small button-text"
                        },
                    )["data-url"]
                    + "pageNumber="
                )
                # print(link)
                alternates = []
                for _ in range(count // 15):
                    print("doing", "https://www.1mg.com" + link + str(_))
                    while 1:
                        try:
                            r2 = requests.get("https://www.1mg.com" + link + str(_))
                            break
                        except:
                            "Bad net, trying again"
                    soup = BeautifulSoup(r2.text, "html.parser")
                    rows = soup.findAll("div", attrs={"class": "row"})
                    for row in rows:
                        brand_name = row.find("a")
                        brand_link = "https://www.1mg.com" + brand_name["href"]
                        brand_name = brand_name.text
                        brand_manufacturer = row.find(
                            "span", attrs={"class": "item-manufacturer"}
                        ).text
                        brand_price = row.find(
                            "div", attrs={"class": "item-price"}
                        ).text
                        try:
                            brand_discount = row.find(
                                "div", attrs={"class": "item-save"}
                            ).text
                        except:
                            brand_discount = ""
                        alternates.append(
                            "||".join(
                                [
                                    brand_name,
                                    brand_link,
                                    brand_manufacturer,
                                    brand_price,
                                    brand_discount,
                                ]
                            )
                        )
            except KeyboardInterrupt:
                pass
            except Exception as e:
                print(e)
                fp = open("alternate_brands_errors.txt", "a+")
                print(entry, end="", file=fp)
                print(
                    "Error has occured in finding alternate brand, url copied to alternate_brands_errors.txt"
                )
            alternates = "PpPpPp".join(alternates)
        print(
            name,
            type,
            manufacturer,
            manufacturer_link,
            salt,
            size,
            introduction,
            price,
            discounted_price,
            discount,
            uses,
            side_effects,
            coping,
            how_to_use,
            how_it_works,
            warnings,
            forget,
            quick_tips,
            faqs,
            feedback,
            references,
            references_links,
            fact_box,
            address,
            alternates,
            sep="~",
            end="\n",
            file=open(input_file_name + "_output.txt", "a", encoding="utf-8"),
        )
    except Exception as e:
        fp = open(input_file_name + "_errors.txt", "w")
        for _ in range(index, len(f1)):
            print(f1[_], end="", file=fp)
        print(
            e,
            "Error has occured, remaining urls copied to",
            input_file_name + "_errors.txt",
        )
        break
fptr.close()
