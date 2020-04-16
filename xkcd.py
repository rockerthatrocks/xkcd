import bs4, requests, sys, os, re

""" 
Downloads the latest xkcd comics
"""

# Make a directory to store the comics
os.makedirs('xkcd', exist_ok=True)

print('Connecting to https://xkcd.com...')
res = requests.get('https://xkcd.com')
res.raise_for_status()
print('Connection successful')

soup = bs4.BeautifulSoup(res.text, 'html.parser')

# Get number of comics to download from command line arguments (defaults to 1)
numberOfComics = 1 if len(sys.argv) != 2 else int(sys.argv[1])

for count in range(numberOfComics):

	print(f'Finding comic #{count+1}...')
	prevLink = soup.select('#comic img')[0].get('src')
	img = requests.get('https:' + prevLink)
	img.raise_for_status()

	# Find the name of the comic
	comicName = re.search(r'/(\w+\.png)$', prevLink)
	
	# Download image
	print(f'Downloading comic #{count+1}...')

	f = open('comics/' + comicName.group(1), 'wb')

	for chunk in img.iter_content(100000):
		f.write(chunk)
	f.close()

	print(f'Download successful')

	# Go to the previous comic
	prev = soup.select('a[rel="prev"]')[0].get('href')
	res = requests.get('https://xkcd.com'+prev)
	res.raise_for_status()
	soup = bs4.BeautifulSoup(res.text, 'html.parser')
