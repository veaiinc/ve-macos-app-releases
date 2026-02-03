#!/usr/bin/env python3
"""Update appcast.xml with new release entry. Called by GitHub Actions."""
import os
import re
from datetime import datetime

def main():
    v = os.environ["VERSION"]
    sv = os.environ["SPARKLE_VER"]
    t = os.environ["TAG"]
    ds = os.environ.get("dmg_size", "0")
    es = os.environ.get("ed_signature", "")
    b = os.environ.get("RELEASE_BODY") or ""
    if not b:
        b = f"<h2>VE v{v}</h2><p>Update available.</p>"
    b = b.replace("]]>", "]]]]><![CDATA[>")

    pd = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S +0000")
    new_entry = f'''        <item>
            <title>{v}</title>
            <pubDate>{pd}</pubDate>
            <link>https://github.com/veaiinc/ve-macos-app-releases/releases</link>
            <sparkle:version>{sv}</sparkle:version>
            <sparkle:shortVersionString>{v}</sparkle:shortVersionString>
            <sparkle:minimumSystemVersion>14.0</sparkle:minimumSystemVersion>
            <description><![CDATA[{b}]]></description>
            <enclosure url="https://github.com/veaiinc/ve-macos-app-releases/releases/download/{t}/VE.dmg" length="{ds}" type="application/octet-stream" sparkle:edSignature="{es}"/>
          </item>
'''
    with open("appcast.xml") as f:
        c = f.read()
    c = re.sub(r'<item>\s*.*?<title>\s*' + re.escape(v) + r'\s*</title>.*?</item>\s*', '', c, flags=re.DOTALL)
    c = re.sub(r'(<channel>\s*\n)', r'\1' + new_entry, c, count=1)
    with open("appcast.xml", "w") as f:
        f.write(c)

if __name__ == "__main__":
    main()
