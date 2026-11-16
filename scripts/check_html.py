"""Sinf sayti uchun oddiy HTML tekshiruvchi (CI shu faylni ishga tushiradi).

Tekshiradi:
  1. Har bir teg to'g'ri yopilganmi.
  2. Har sahifada <title> bormi.
  3. Kodda parol yoki maxfiy kalit qolib ketmaganmi.
  4. Konflikt belgilari (<<<<<<<, =======, >>>>>>>) unutilib qolmaganmi.
"""
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

VOID_TAGS = {"area", "base", "br", "col", "embed", "hr", "img", "input",
             "link", "meta", "source", "track", "wbr"}
CONFLICT = re.compile(r"^(<{7}|={7}|>{7})( |$)")
SECRET = re.compile(r"(api[_-]?key|password|parol|secret|token)\s*[:=]\s*['\"]?\w+", re.IGNORECASE)


class TagChecker(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack = []
        self.errors = []
        self.has_title = False

    def handle_starttag(self, tag, attrs):
        if tag == "title":
            self.has_title = True
        if tag not in VOID_TAGS:
            self.stack.append((tag, self.getpos()[0]))

    def handle_endtag(self, tag):
        if tag in VOID_TAGS:
            return
        if not self.stack:
            self.errors.append(f"{self.getpos()[0]}-qator: </{tag}> bor, lekin <{tag}> ochilmagan")
            return
        open_tag, line = self.stack.pop()
        if open_tag != tag:
            self.errors.append(
                f"{self.getpos()[0]}-qator: </{tag}> kutilmagan, {line}-qatordagi <{open_tag}> hali yopilmagan")
            self.stack.append((open_tag, line))
            if any(t == tag for t, _ in self.stack):
                while self.stack and self.stack[-1][0] != tag:
                    self.stack.pop()
                if self.stack:
                    self.stack.pop()


def check_file(path):
    text = path.read_text(encoding="utf-8")
    checker = TagChecker()
    checker.feed(text)
    errors = list(checker.errors)
    for tag, line in checker.stack:
        errors.append(f"{line}-qatordagi <{tag}> yopilmagan")
    if not checker.has_title:
        errors.append("<title> yo'q: har sahifaga sarlavha kerak")
    for number, line in enumerate(text.splitlines(), start=1):
        if SECRET.search(line):
            errors.append(f"{number}-qator: parol yoki maxfiy kalitga o'xshash matn bor")
        if CONFLICT.match(line.strip()):
            errors.append(f"{number}-qator: konflikt belgisi qolib ketgan, hal qilib o'chiring")
    return errors


def main():
    root = Path(__file__).resolve().parent.parent
    files = sorted(p for p in root.rglob("*.html") if ".git" not in p.parts)
    failed = 0
    for path in files:
        errors = check_file(path)
        name = path.relative_to(root)
        if errors:
            failed += 1
            print(f"XATO  {name}")
            for e in errors:
                print(f"      - {e}")
        else:
            print(f"OK    {name}")
    print(f"\nJami: {len(files)} ta fayl, {failed} tasida xato.")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
