# -*- coding: utf-8 -*-
"""
@author: 51takahashi
"""

from pathlib import Path
import os
import requests

conf = 'CVPR2019'
header = 'http://openaccess.thecvf.com/'

def name_check(name):
    name = name.replace('?','')
    name = name.replace(':','')
    name = name.replace('*','')
    name = name.replace('\"','')
    name = name.replace('/',' or ')
    return name

def main():
    if not os.path.exists(conf):
        os.mkdir(conf)
    r = requests.get(header+conf+'.py')
    txt = r.text;
    lines = txt.split('\n')
    cnt = 0

    existing_files = [f.stem for f in Path(conf).glob('*.pdf')]

    for line in lines:
        if line.find('<dt class="ptitle">')>-1:
            pdfname = conf+'/'+name_check(line.split('>')[3].split('<')[0])+'.pdf'
            cnt+=1

        if len(line)>0:
            if line[0]=='[':
                print(str(cnt)+':'+pdfname)

                if pdfname.replace('.pdf', '') in existing_files:
                    continue

                if not os.path.exists(pdfname):
                    url = header+line.split('"')[1]
                    r = requests.get(url)
                    f = open(pdfname, 'wb')
                    f.write(r.content)
                    f.close()

if __name__ == '__main__':
    main()
