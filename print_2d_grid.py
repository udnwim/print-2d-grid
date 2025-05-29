import requests
from bs4 import BeautifulSoup

def extract_google_doc_content(url):
    response = requests.get(url)
    if response.status_code != 200:
        print("Failed to fetch the document.")
        return

    soup = BeautifulSoup(response.text, 'html.parser')

    body = soup.find('body')
    if not body:
        print("No body content found.")
        return

    # pull data from google doc table and form a list of tuples
    data = []
    for table in body.find_all('table'):
      rows = table.find_all('tr')
      for row in rows[1:]:
          temp = []
          for cell in row.find_all(['td', 'th']):
              text = cell.get_text(strip=True)
              try:
                  value = int(text)
              except ValueError:
                  value = text
              temp.append(value)
          char_location = tuple(temp)
          data.append(char_location)

    # create the grid and print
    width = max(x for x, _, _ in data) + 1
    height = max(y for _, _, y in data) + 1
    # print (width, height)

    grid = [[' ' for _ in range(width)] for _ in range(height)]

    for x, char, y in data:
        grid[height - 1 - y][x] = char

    for row in grid:
        print(''.join(row))



url = "https://docs.google.com/document/d/e/2PACX-1vQGUck9HIFCyezsrBSnmENk5ieJuYwpt7YHYEzeNJkIb9OSDdx-ov2nRNReKQyey-cwJOoEKUhLmN9z/pub"
extract_google_doc_content(url)