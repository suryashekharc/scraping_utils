from bs4 import BeautifulSoup
import requests
import pickle


def get_all_links_from_telegraph(tag="citizenship-amendment-act-2019-caa", dump_pickle=True):
    """

    :param tag:         Tag of the articles to search for, string
    :param dump_pickle: Whether to dump the list of links as a pickle file, boolean
    :return:            A list of links for the given tag, list of strings
    """
    list_of_page_titles = ['https://www.telegraphindia.com/topic/' + str(tag) + "?&page='+ \
                            str(page_num) for page_num in range(1, 51)]
    list_of_links = []
    for page_of_titles in list_of_page_titles:
        page = requests.get(page_of_titles)
        page_indexed = BeautifulSoup(page.text, 'html.parser')
        page_indexed_topics = page_indexed.find_all("ul", class_="listing-withImage")[0].find_all("h3")
        page_indexed_hrefs = ['https://www.telegraphindia.com'+elem['href'] for page in page_indexed_topics
                              for elem in page.find_all(href=True)]
        list_of_links.extend(page_indexed_hrefs)
    print("Total number of links: {}".format(len(list_of_links)))
    with open('href_list_telegraph.pickle', 'wb') as handle:
        pickle.dump(list_of_links, handle)
    return list_of_links


def get_telegraph_corpus(pickle_file_name="href_list_telegraph.pickle",
                         tag="citizenship-amendment-act-2019-caa",
                         dump_pickle=True):
    """

    :param pickle_file_name: Pickle file name, if it exists, string
    :param tag:              Tag of the articles to search for, string
    :param dump_pickle:      Whether to dump the list of dicts as a pickle file, boolean
    :return:
    """
    if pickle_file_name:
        with open('href_list_telegraph.pickle', 'rb') as handle:
            all_links = pickle.load(handle)
    else:
        all_links = get_all_links_from_telegraph(tag)

    list_of_dicts = []
    for one_link in all_links:
        print(one_link)
        page = requests.get(one_link)
        page_indexed = BeautifulSoup(page.text, 'html.parser')
        story_content = page_indexed.findAll('div', attrs={"class": "storyviewContent"})
        if story_content:
            story_text = ' '.join([para.text for para in story_content[0].findAll('p')])
            author_location = [p.text for p in page_indexed.find_all("div", class_="author-name")]
            if author_location:
                author_location = author_location[0]
            else:
                author_location = "Not Available"
            page_dict = {'text': story_text.strip(),
                         'link': one_link.strip(),
                         'author_location': author_location.strip()}
            list_of_dicts.append(page_dict)
    if dump_pickle:
        with open('corpus_telegraph_all.pickle', 'wb') as handle:
            pickle.dump(list_of_dicts, handle)
    return list_of_dicts


if __name__ == '__main__':
    get_telegraph_corpus(pickle_file_name=None)  # Run this the first time
    # get_telegraph_corpus()  # Run this next time onwards
