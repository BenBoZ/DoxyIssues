#! /usr/bin/env python

from githubpy.github import *

from textwrap import TextWrapper

import argparse

__doc__ = """\
doxy_issues retrieves all github issues from the given repo and outputs them in 
MarkDown format which is suitable for Doxygen.
"""

# constants
REQ_TEMPLATE = """\n\
    | {requirement_txt}:{title_txt} {labels_txt} |
    |-{sep_col}-|\n\
{body_txt}

"""
EMPTY_ROW = """\
    | """


def get_all_issues(user, repo, state='all'):
    "Gets all issues from the specified users repo"

    gh = GitHub()

    page = 1
    issues = []
    while True:
        result = gh.repos(user)(repo).issues.get(state=state, page=str(page))
        if len(result) > 0:
            print('Retrieved page {}'.format(page))
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

def write_file_to_disk(output_path, output_string):
    " write the formatted file to disk "

    f = open(output_path,"w")
    f.write(output_string)
    f.close()

def parse_arguments():
    """ Parses the arguments given """

    parser = argparse.ArgumentParser(description = __doc__)

    parser.add_argument('-u','--user', default='BenBoZ', type=str, 
                        help='The user or organization of the repo') 

    parser.add_argument('-r','--repo', default='DoxyIssues', type=str, 
                        help='The name of the repo')

    parser.add_argument('-s','--state', default='all', type=str,
                        choices=['open','closed','all'],
                        help='Define in which state the issues are in')

    parser.add_argument('-o','--output_path', default='output.dox', type=str,
                        help='The relative or absolute path where the file will be written')

    return parser.parse_args()

if __name__ == "__main__":

    args = parse_arguments()

    print("Getting {0.state} issues from https://github/com/{0.user}/{0.repo}".format(args))

    issues = get_all_issues(args.user, args.repo, args.state)

    output_file = create_header()
    ref_links = {}

    for issue in issues:
        formatted_issue, ref_links = format_issue(issue, ref_links)
        output_file += formatted_issue
        output_file += create_seperator()

    output_file += create_footer(ref_links)

    print("Writing issues to {0.output_path}".format(args))
    write_file_to_disk(args.output_path, output_file)

