import os
import click
import tempfile
from whoosh import index as idx
from whoosh.lang import NoStemmer, NoStopWords, languages
from whoosh.fields import Schema, TEXT, ID
from whoosh.qparser import QueryParser
from whoosh.analysis import SimpleAnalyzer, CharsetFilter
from whoosh.highlight import Formatter
from whoosh.analysis.morph import StemFilter
from whoosh.support.charset import accent_map
from whoosh.analysis.filters import StopFilter
from blessings import Terminal


try:
    NotFound = FileNotFoundError
    IsDirectory = IsADirectoryError
except NameError:
    NotFound = IOError
    IsDirectory = IOError

color = Terminal()

dir = None

defaultdir = os.path.join(tempfile.gettempdir(), 'washer_index')
defaultlangs = {'en', 'pt'}
lang = os.getenv('LANG', '')[:2]
if lang:
    defaultlangs.add(lang)


@click.group()
@click.option('--indexdir', '-d',
              type=click.Path(file_okay=False, writable=True),
              default=defaultdir,
              help='The directory in which the index files will be kept. '
                   'Defaults to a temporary directory.')
def main(indexdir):
    global dir
    dir = indexdir

    if not os.path.exists(dir):
        os.makedirs(dir)


@main.command()
@click.option('--lang', '-l',
              type=click.Choice(languages),
              multiple=True,
              default=defaultlangs,
              help='Comma-separated list of languages to use when indexing. '
                   'Should be specified multiple times. '
                   'Defaults to "{}".'.format(
                        ' '.join('-l ' + l for l in defaultlangs)
                    )
              )
@click.argument('files_to_index', type=click.Path(), nargs=-1)
def index(lang, files_to_index):
    chain = SimpleAnalyzer()
    for l in lang:
        lang = l.strip()
        try:
            chain = chain | StopFilter(lang=lang, maxsize=40)
        except NoStopWords:
            pass
        try:
            chain = chain | StemFilter(lang=lang)
        except NoStemmer:
            pass
    chain = chain | CharsetFilter(accent_map)
    schema = Schema(path=ID(stored=True), content=TEXT(analyzer=chain))

    ix = idx.create_in(dir, schema)
    writer = ix.writer()

    nindexed = 0
    for path in files_to_index:
        click.echo('indexing {}'.format(path))
        try:
            with open(path, 'rb') as f:
                content = readfile(f)
                writer.add_document(path=path, content=content)
            nindexed += 1
        except (NotFound, IsDirectory):
            click.echo('  not found.')

    if nindexed:
        writer.commit()
        click.echo('{} files indexed. index created at {}'
                   .format(nindexed, dir))
    else:
        click.echo('no files were indexed.')


@main.command()
@click.argument('query', type=str, nargs=-1)
def search(query):
    query = ' '.join(query)
    click.echo('searching for {}...'.format(color.green(query)))

    ix = idx.open_dir(dir)
    with ix.searcher() as searcher:
        query = QueryParser('content', ix.schema).parse(query)
        results = searcher.search(query)
        results.fragmenter.charlimit = 1000000
        results.fragmenter.maxchars = 200
        results.fragmenter.surround = 30
        results.formatter = ShellFormatter()
        for hit in results:
            click.echo('  {}'.format(color.magenta_bold(hit['path'])))
            try:
                with open(hit['path'], 'rb') as f:
                    content = readfile(f)
                    click.echo(hit.highlights('content', text=content, top=5))
            except NotFound:
                pass


class ShellFormatter(Formatter):
    def format(self, fragments, replace=False):
        out = []
        for f in fragments:
            out.append('    ' + self.format_fragment(f))
        return '\n'.join(out)

    def format_fragment(self, fragment):
        text = fragment.text[fragment.startchar:fragment.endchar]

        shifted = fragment.startchar
        output = ''
        for match in fragment.matches:
            output += color.cyan
            start = match.startchar - shifted
            output += text[:start]
            text = text[start:]
            shifted += start

            output += color.green_underline
            end = match.endchar - shifted
            output += text[:end]
            text = text[end:]
            shifted += end
            output += color.normal

        output += color.cyan
        output += text
        output += color.normal

        return output \
            .replace('\n\r', '¶ ') \
            .replace('\r', '¶ ') \
            .replace('\n', '¶ ')


def readfile(f):  # this expects a file object opened with open(<path>, 'rb')
    bytecontents = f.read()
    for tryencoding in ['utf-8', 'cp1252', 'latin_1', 'euc-jp',
                        'gb2312', 'cp1251', 'sjis', 'iso-8859-2']:
        try:
            return bytecontents.decode(tryencoding)
        except UnicodeDecodeError:
            pass
    else:
        return bytecontents.decode('ascii', 'ignore')


if __name__ == '__main__':
    main()
