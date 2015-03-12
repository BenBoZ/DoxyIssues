#! /usr/bin/env python

from githubpy.github import *

from textwrap import TextWrapper

USER='RemediOSM'
REPO='UltraSound'

USER='syncthing'
REPO='syncthing'

OUTPUT_FILE = "output.txt"

REQ_TEMPLATE = """\n\
    | {requirement_txt}:{title_txt} {labels_txt} |
    |-{sep_col}-|\n\
{body_txt}

"""
EMPTY_ROW = """\
    | """

def get_all_issues(user, repo):
    "Gets all issues from the specified users repo"

    gh = GitHub()

    page = 1
    issues = []
    while True:
        print('page {}'.format(page))
        result = gh.repos(USER)(REPO).issues.get(state='all')
        if len(result) > 0:
            issues = issues + result
            page += 1
        else:
            break

    return issues


def format_issue(issue, ref_links):
    "Returns a formatted issue"

    requirement, ref_links = format_requirement(issue, ref_links)

    labels, ref_links = format_labels(issue, ref_links)


    width_col = len(requirement)+len(labels)+len(issue['title']) + 2

    body = format_body(issue, EMPTY_ROW, width_col)

    formatted_issue = REQ_TEMPLATE.format(requirement_txt=requirement,
                                          title_txt=issue['title'],
                                          labels_txt=labels,
                                          body_txt=body,
                                          sep_col='-'*width_col)

    return formatted_issue, ref_links

def format_body(issue, empty_row, width_col):

    wrapper = TextWrapper(initial_indent = empty_row,
                          subsequent_indent = empty_row,
                          width=len(empty_row) + width_col,
                          replace_whitespace=False)

    body = issue['body'].replace('\n', ' '*width_col)

    lines = wrapper.wrap(body)
    txt = ""

    for line in lines:
       txt += line.ljust(width_col + len(empty_row) ) + (' |\n')

    return txt

def format_requirement(issue, ref_links):

    req_url_ref = "req_{}_url".format(issue['number'])
    req_name = "requirement {}".format(issue['number'])

    formatted_requirement, ref_links = _create_link(req_name, req_url_ref, issue['html_url'], ref_links)

    return formatted_requirement, ref_links

def format_labels(issue, ref_links):

    formatted_labels = ""

    for label in issue['labels']:
        if formatted_labels: formatted_labels += " "

        label_url_ref = "{}_url".format(label['name'])
        ref_links[label_url_ref] = label['url']

        formatted_lbl, ref_links = _create_link(label['name'], label_url_ref, label['url'], ref_links)
        formatted_labels += formatted_lbl

    return formatted_labels, ref_links

def _create_link(name, ref_name, url, ref_links):

    ref_links[ref_name] = url

    formatted_link = "[{}][{}]".format(name, ref_name)

    return formatted_link, ref_links

def create_header():
    "Returns header for top of page"

    header = "/*! \page requirements Requirements\n\n"

    return header

def create_footer(ref_links):
    "Returns footer for bottom of page"

    footer = "\n"

    for ref, url in ref_links.items():
        footer += "[{ref}]: {url}\n".format(ref=ref, url=url)

    footer += "\n*/\n"

    return footer

def create_seperator():
    return "\n"

def write_file_to_disk(output_string):
    " write the formatted file to disk "

    f = open(OUTPUT_FILE,"w")
    f.write(output_string)
    f.close()

if __name__ == "__main__":

    issues = get_all_issues(USER, REPO)

    output_file = create_header()
    ref_links = {}

    for issue in issues:
        formatted_issue, ref_links = format_issue(issue, ref_links)
        output_file += formatted_issue
        output_file += create_seperator()

    output_file += create_footer(ref_links)

    write_file_to_disk(output_file)

