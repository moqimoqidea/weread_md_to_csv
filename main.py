import csv
from pathlib import Path


def get_title_and_author(source):
    line_array = open(source, 'r', encoding='utf-8').readlines()
    title = line_array[0][2:-1]
    author = line_array[2][3:-3]
    return title, author


def markdown_to_csv(source, target):
    csv_header = ['Highlight', 'Chapter', 'Title', 'Author', 'Note']
    csv_data = []

    title_author_tuple = get_title_and_author(source)
    title, author = title_author_tuple[0], title_author_tuple[1]

    txt = Path(source).read_text()
    chapters = txt.split('###')

    for chapter in chapters:
        if chapter[0] != ' ':
            continue

        rows = chapter.split('\n\n')
        chapter_name = rows[0][1:]

        if chapter_name == '最终点评':
            csv_data.append(['', chapter_name, title, author, rows[1][2:]])
            continue

        for row in rows[1:-1]:
            if row.startswith('* '):
                highlight = row[2:]
            elif row.startswith('\n* '):
                highlight = row[3:]
            else:
                continue

            if highlight.count('（个人笔记:') != 0:
                note = highlight[highlight.index('（个人笔记:') + 7:][:-1]
            else:
                note = ''

            csv_data.append([highlight, chapter_name, title, author, note])

    with open(target, 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(csv_header)

        for row in csv_data:
            writer.writerow(row)


if __name__ == '__main__':
    markdown_to_csv('test_data/source.md', 'test_data/target.csv')
