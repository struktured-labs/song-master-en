import json,sys
s=json.load(open('/workspace/song-master-en/script/jp/strings.json'))
for b in sys.argv[1:]:
  for x in s:
    if x['first'][:3]==b: print(x['uid'],x['text'].replace('[pause]','').replace('\u3000','_'))
