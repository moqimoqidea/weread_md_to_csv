import csv
from pathlib import Path

if __name__ == '__main__':
    header = ['Highlight', 'Chapter', 'Title', 'Author', 'Note']
    data = []

    source = 'test_data/source.md'
    target_v1 = 'test_data/target_v1.csv'

    line_array = open(source, 'r', encoding='utf-8').readlines()
    title = line_array[0][2:-1]
    print(title)
    author = line_array[2][3:-3]
    print(author)

    txt = Path(source).read_text()

    chapters = txt.split('###')
    print(len(chapters))

    for chapter in chapters:
        # skip non standard chapters
        if chapter[0] != ' ':
            continue

        rows = chapter.split('\n\n')
        chapter_name = rows[0][1:]
        print(chapter_name)

        for row in rows[1:-1]:
            highlight = ''
            note = ''

            if row.startswith('* '):
                highlight = row[2:]
            elif row.startswith('\n* '):
                highlight = row[3:]
            else:
                continue

            print(highlight)

            if highlight.count('（个人笔记:') != 0:
                note = highlight[highlight.index('（个人笔记:') + 7:][:-1]
                print(note)

            data.append([highlight, chapter_name, title, author, note])

    print(len(data))
    print(data)

    with open(target_v1, 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(header)

        for row in data:
            writer.writerow(row)
