import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    probabilities = {
        namePage: 0
        for namePage in corpus
    }

    if corpus[page] == set():
        for namePage in probabilities:
            probabilities[namePage] = 1 / len(probabilities)
    
    else:
        for namePage in corpus[page]:
            probabilities[namePage] += damping_factor / len(corpus[page])

        for namePage in probabilities:
            probabilities[namePage] += (1 - damping_factor) / len(probabilities)

    return probabilities


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Store the number of visits in each page
    pages = {
        namePage: 0
        for namePage in corpus
    }
    
    currentPage = random.choice(list(corpus.keys()))
    pages[currentPage] += 1

    for i in range(n-1):
        probabilities = transition_model(corpus, currentPage, damping_factor)

        rand = random.randint(1, 100)

        total = 0
        for namePage in probabilities:
            total += probabilities[namePage] * 100

            if rand <= total:
                currentPage = namePage
                break

        pages[currentPage] += 1

    pageRank = {
        namePage: pages[namePage] / n
        for namePage in corpus
    }

    return pageRank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    initRank = 1 / len(corpus)
    randomChoiceProb = (1 - damping_factor) / len(corpus)
    iterations = 0

    # Initial pageRank gives every page a rank of 1/(num pages in corpus)
    pageRank = {
        namePage: initRank 
        for namePage in corpus
    }
    newRanks = {
        namePage: None 
        for namePage in corpus
    }

    maxPageRankChange = initRank
    # Iteratively calculate page rank until no change > 0.001
    while maxPageRankChange > 0.001:
        iterations += 1
        maxPageRankChange = 0

        for namePage in corpus:
            surfChoiceProb = 0

            for other_page in corpus:
                # If other page has no links it picks randomly any corpus page:
                if len(corpus[other_page]) == 0:
                    surfChoiceProb += pageRank[other_page] * initRank

                # Else if other_page has a link to namePage, it randomly picks from all links on other_page:
                elif namePage in corpus[other_page]:
                    surfChoiceProb += pageRank[other_page] / len(corpus[other_page])
            
            # Calculate new page rank
            newRank = randomChoiceProb + (damping_factor * surfChoiceProb)
            newRanks[namePage] = newRank

        # Normalise the new page ranks:
        norm_factor = sum(newRanks.values())
        newRanks = {
            namePage: (rank / norm_factor) 
            for namePage, rank in newRanks.items()
        }

        # Find max change in page rank:
        for namePage in corpus:
            rank_change = abs(pageRank[namePage] - newRanks[namePage])

            if rank_change > maxPageRankChange:
                maxPageRankChange = rank_change

        # Update page ranks to the new ranks:
        pageRank = newRanks.copy()

    return pageRank


if __name__ == "__main__":
    main()
