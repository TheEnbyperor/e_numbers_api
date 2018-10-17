from bs4 import BeautifulSoup
import requests
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "e_number_api.settings")
django.setup()

# your imports, e.g. Django models
from src.api.models import Category, Substance, SubstanceMoreInfo

base_url = "https://en.wikipedia.org"

page = requests.get("https://en.wikipedia.org/wiki/E_number")
soup = BeautifulSoup(page.content, 'html.parser')

table_id = "E1000–E1599_(additional_additives)"
category = Category.objects.get(name="Additional additives")
sub_categories = category.sub_categories.all()

heading = soup.find(id=table_id).parent
table = heading.findNext('table').tbody
rows = table.find_all('tr')[1:]
for row in rows:
    cols = row.find_all('td')
    e_number = cols[0].text.strip().replace('E', '')
    name = cols[1].text.strip()
    links = cols[1].find_all('a')
    links = list(map(lambda l: (l.text.capitalize(), base_url + l.attrs["href"]), links))
    print(f"Substance: {e_number}: {name}")
    print(f"More info: {links}")
    print("Sub categories:")
    for i, s in enumerate(sub_categories):
        print(f"- {i}: {s.name}")
    sub_category = None
    while sub_category is None:
        try:
            category = input("Select sub category:")
            if category == "s":
                break
            sub_category = sub_categories[int(category)]
        except ValueError:
            continue
    if sub_category is None:
        continue
    substance = Substance()
    substance.name = name
    substance.e_number = e_number
    substance.sub_category = sub_category
    substance.save()
    for l in links:
        more_info = SubstanceMoreInfo()
        more_info.substance = substance
        more_info.name = l[0]
        more_info.more_info = l[1]
        more_info.save()
