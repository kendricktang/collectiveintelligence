import feedparser
import re


def getwordcounts(url):
    # Parse the feed
    site = feedparser.parse(url)
    word_count = {}
    try:
        title = site.feed.title
    except AttributeError:
        return '', ''

    # Loop over all the entries in the url
    for entry in site.entries:
        if 'summary' in entry:
            summary = entry.summary
        else:
            summary = entry.description

        # Extract words
        words = getwords(entry.title+' '+summary)
        for word in words:
            word_count.setdefault(word, 0)
            word_count[word] += 1

    return title, word_count


def getwords(html):
    # Remove all HTML tags
    txt = re.compile(r'<[^>]+>').sub('', html)

    # Split by all nonalpha characters
    words = re.compile(r'[^A-Z^a-z]+').split(txt)

    # Convert to lowercase
    return [word.lower() for word in words if word]

if __name__ == '__main__':
    appear_count = {}
    word_counts = {}
    numofurls = 0
    for feedurl in file('data/feedlist.txt'):
        numofurls += 1
        print 'Progress: ' + str(numofurls)
        title, word_count = getwordcounts(feedurl)
        if title is '':
            continue
        word_counts[title] = word_count
        for word, count in word_count.items():
            appear_count.setdefault(word, 0)
            if count > 1:
                appear_count[word] += 1

    # Only consider words that appear between 10% and 50% of the URLs.
    # Otherwise, they're too rare, or way too common,
    # and as a result aren't interesting.
    wordlist = []
    for word, count in appear_count.items():
        frac = float(count)/numofurls
        if frac > 0.1 and frac < 0.5:
            wordlist.append(word)

    # Write output file
    out = file('data/blogdata.txt', 'w')
    out.write('Blog')
    for word in wordlist:
        out.write('\t%s' % word)
    out.write('\n')
    for blog, word_count in word_counts.items():
        out.write(blog)
        for word in wordlist:
            if word in word_count:
                out.write('\t%d' % word_count[word])
            else:
                out.write('\t0')
        out.write('\n')
