import csv
import os
import sys
from pathlib import Path


def get_title_and_author(source):
    line_array = open(source, 'r', encoding='utf-8').readlines()
    title = line_array[0][2:-1]
    author = line_array[2][3:-3]
    return title, author


def markdown_to_csv(source, target):
    title_author_tuple = get_title_and_author(source)
    title, author = title_author_tuple[0], title_author_tuple[1]

    csv_data = []
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
        writer.writerow(['Highlight', 'Chapter', 'Title', 'Author', 'Note'])

        for row in csv_data:
            writer.writerow(row)


if __name__ == '__main__':
    first_argv = sys.argv[1]

    if first_argv == '-h':
        print('Usage: python main.py source.md target.csv')
        sys.exit(0)

    if not os.path.exists(first_argv):
        print('Path: {} does not exist.'.format(first_argv))
        sys.exit(0)

    if os.path.isdir(first_argv):
        print('Path: {} is a directory.\n'.format(first_argv))
        list_file = os.listdir(first_argv)
        for file in list_file:
            if file.endswith('.md'):
                print('Converting {} to csv...'.format(file))
                markdown_to_csv(first_argv + '/' + file, first_argv + '/' + file[:-2] + 'csv')
        print('\nAll md converting Done.')
        sys.exit(0)

    if not first_argv.endswith('.md'):
        print('File: {} is not a markdown file.'.format(first_argv))
        sys.exit(0)

    source_md = first_argv
    target_csv = first_argv[:-2] + 'csv'
    if len(sys.argv) >= 3:
        target_csv = os.path.dirname(source_md) + '/' + sys.argv[2]
    else:
        target_csv = source_md[:-2] + 'csv'

    markdown_to_csv(source_md, target_csv)
    print('Converting {} to csv {}, done'.format(source_md, target_csv))
