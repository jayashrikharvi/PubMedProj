# Python script that uses Biopython library to search PubMed for abstracts related to a specific keyword

import argparse
import csv
from Bio import Entrez

# tell NCBI who you are
Entrez.email = "jaikharvi@gmail.com"

#PubMed can be searched using the Entrez Programming Utilities (E-utilities), provided by the NCBI
def search(query):
    handle = Entrez.esearch(db='pubmed',
                            sort='relevance',
                            retmax='50', #searches PubMed for the 50 most relevant articles
                            retmode='xml',
                            term=query)
    results = Entrez.read(handle)
    handle.close()
    return results

def fetch_details(id_list):
    ids = ','.join(id_list)
    handle = Entrez.efetch(db='pubmed',
                           retmode='xml',
                           id=ids)
    results = Entrez.read(handle)
    handle.close()
    return results

def save_to_csv(results, filename):
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['Title', 'PMID', 'Link']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for paper in results['PubmedArticle']:
            title = paper['MedlineCitation']['Article']['ArticleTitle']
            pmid = paper['MedlineCitation']['PMID']
            link = f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
            writer.writerow({'Title': title, 'PMID': pmid, 'Link': link})

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Search PubMed via the command line')
    parser.add_argument('query', type=str, help='The search query for PubMed')
    parser.add_argument('filename', type=str, help='Filename for output CSV')
    args = parser.parse_args()

    search_results = search(args.query)
    id_list = search_results['IdList']
    papers = fetch_details(id_list)
    save_to_csv(papers, args.filename)
