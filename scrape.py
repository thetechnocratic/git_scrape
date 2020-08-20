import sys
import urllib.request
from bs4 import BeautifulSoup
from collections import OrderedDict
from pprint import pprint
import subprocess
import git

git_clone = "git clone %s"

def scrape(url, output_dir):
    response = urllib.request.urlopen(url)
    html = response.read()

    soup = BeautifulSoup(html, 'lxml')

    for link in soup.find("div", {"id": "org-repositories"}).find_all("a", {"itemprop": "name codeRepository"}):
        base_link = link.get('href').strip()
        git_link = "https://github.com" + base_link + ".git"
        out_dir = output_dir + '/' + link.getText().strip()
        
        process = subprocess.Popen(['mkdir', out_dir], stdout=subprocess.PIPE)
        output, error = process.communicate()
        # print(output)
        
        print(out_dir)
        print(git_link)
        print('ok')
        git.Git(out_dir).clone(git_link)

    with open('./output.html', 'w') as f:
        f.write(html.decode('utf-8'))

    # d = OrderedDict()
    # for th, td in zip(soup.select('th'), soup.select('td')[::2]):
    #     d[th.text.strip()] = td.text.strip().splitlines()

    # pprint(d)


if __name__ == "__main__":
    giturl = sys.argv[1]
    print(giturl)
    output_dir = sys.argv[2]
    scrape(giturl, output_dir)