from bs4 import BeautifulSoup
import requests
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "e_number_api.settings")
django.setup()

# your imports, e.g. Django models
from src.api.models import Category, SubCategory, SubCategoryMoreInfo

base_url = "https://en.wikipedia.org"

page = requests.get("https://en.wikipedia.org/wiki/E_number")
soup = BeautifulSoup(page.content, 'html.parser')

table_id = "Classification_by_numeric_range"
categories = Category.objects.all()

heading = soup.find(id=table_id).parent
table = heading.next_sibling.next_sibling.tbody
rows = table.find_all('tr')[1:]
for row in rows:
    cols = row.find_all('td')
    if cols[0].attrs.get("rowspan") is not None:
        cols = cols[1:]
    e_number = cols[0].text.strip()
    name = cols[1].text.strip().capitalize()
    links = cols[1].find_all('a')
    links = list(map(lambda l: (l.text.capitalize(), base_url + l.attrs["href"]), links))
    print(f"Sub category: {e_number}: {name}")
    print(f"More info: {links}")
    print("Categories:")
    for s in categories:
        print(f"- {s.id}: {s.name}")
    category = input("Select category:")
    if category == "s":
        continue
    category = Category.objects.get(id=category)
    sub_category = SubCategory()
    sub_category.category = category
    sub_category.name = name
    sub_category.save()
    for l in links:
        more_info = SubCategoryMoreInfo()
        more_info.sub_category = sub_category
        more_info.name = l[0]
        more_info.more_info = l[1]
        more_info.save()
