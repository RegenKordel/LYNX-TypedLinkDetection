from export import data_access
import logging
import pandas as pd
import itertools
import collections
from collections import Counter, defaultdict
import statistics
import itertools
import re
import math
from pprint import pprint
from bs4 import BeautifulSoup as Soup
import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def extract_issue_csv(project):
    client = data_access.MongoDBConnection(host='localhost', port=27017,
                                           auth_mechanism=None, auth_source=None,
                                           password=None, username=None,
                                           connect_timeout=5000).client
    db = client['JiraRepos']
    source_collection = db[project]
    cursor = source_collection.find({})

    d = {'issue_id': [],
         'type': [],
         'status': [],
         'priority': [],
         'resolution': [],
         'projectid': [],
         'created': [],
         'updated': [],
         'description': [],
         'title': [],
         'components': [],
         }

    i = 0

    for issue in cursor:
        try:
            issue_key = issue['key']
            logging.info(issue_key)

            try:
                issuetype = issue['fields']['issuetype']['name']
            except Exception:
                issuetype = 'None'

            try:
                status = issue['fields']['status']['name']
            except Exception:
                status = 'None'
            try:
                priority = issue['fields']['priority']['name']
            except Exception:
                priority = 'None'
            projectid = issue['fields']['project']['name']
            try:
                resolution = issue['fields']['resolution']['name']
            except Exception:
                resolution = 'Open'

            try:
                componentsArray = issue['fields']['components']
                component = ""
                for i in range(0, len(componentsArray)):
                    component = component + i['name']

            except Exception:
                component = ''

            try:
                created = issue['fields']['created']
            except Exception:
                created = 'No creation date'
            try:
                updated = issue['fields']['updated']
            except Exception:
                updated = 'No update date'

            try:
                description = issue['fields']['description']
            except Exception:
                description = ''
            try:
                title = issue['fields']['summary']
            except Exception:
                title = ''

            d['issue_id'].append(issue_key)

            d['type'].append(issuetype)
            d['status'].append(status)
            d['priority'].append(priority)
            d['resolution'].append(resolution)
            d['projectid'].append(projectid)
            d['components'].append(component)

            d['created'].append(created)
            d['updated'].append(updated)

            d['description'].append(description)
            d['title'].append(title)

            logging.info("SUCCESS")

            i += 1
            logging.info(i)

        except Exception as e:
            logging.info("!!ERROR!!ERROR!!ERROR!!ERROR!!ERROR!!ERROR!!ERROR!!")
            pass
    logging.info(f'Creating csv.')
    df = pd.DataFrame.from_dict(d)
    # adapt file path
    filename = '~data/raw/issues_' + project.lower() + '.csv'
    logging.info(filename)
    df.to_csv(filename, sep=';', index=False)
    return None


def extract_links_csv(project):
    client = data_access.MongoDBConnection(host='localhost', port=27017,
                                           auth_mechanism=None, auth_source=None,
                                           password=None, username=None,
                                           connect_timeout=5000).client
    db = client['JiraRepos']
    source_collection = db[project]
    cursor = source_collection.find({})

    d = {'name': [],
         'linktype': [],
         'issue_id_1': [],
         'issue_id_2': [],
         }
    epiclinkfield_dict = {'Apache': 'customfield_12311120',
                          'Hyperledger': 'customfield_10006',
                          'IntelDAOS': 'customfield_10092',
                          'JFrog': 'customfield_10806',
                          'Jira': 'customfield_12931',
                          'JiraEcosystem': 'customfield_12180',
                          'MariaDB': 'customfield_10600',
                          'MindVille': 'customfield_10000',
                          'MongoDB': 'customfield_10857',
                          'Qt': 'customfield_10400',
                          'Redhat': 'customfield_12311140',
                          'Sakai': 'customfield_10772',
                          'SecondLife': 'customfield_10871',
                          'Sonatype': 'customfield_11500',
                          'Spring': 'customfield_10680'
                          }

    for issue in cursor:
        try:
            issue_key = issue['key']
            logging.info(issue_key)

            if project == 'RedHat':
                try:
                    parent = issue['fields']['customfield_12313140']
                    inwardIssue = issue_key
                    outwardIssue = parent
                    linktype = 'Parent-Relation'
                    name = inwardIssue + "_" + outwardIssue

                    d['name'].append(name)
                    d['linktype'].append(linktype)
                    d['issue_id_1'].append(inwardIssue)
                    d['issue_id_2'].append(outwardIssue)
                except Exception:
                    logging.info("no parents")

                try:
                    feature = issue['fields']['customfield_12318341']
                    inwardIssue = issue_key
                    outwardIssue = feature
                    linktype = 'Feature-Relation'
                    name = inwardIssue + "_" + outwardIssue

                    d['name'].append(name)
                    d['linktype'].append(linktype)
                    d['issue_id_1'].append(inwardIssue)
                    d['issue_id_2'].append(outwardIssue)
                except Exception:
                    logging.info("no features")

            try:
                epic = issue['fields'][epiclinkfield_dict[project]]
                inwardIssue = issue_key
                outwardIssue = epic
                linktype = 'Epic-Relation'
                name = inwardIssue + "_" + outwardIssue

                d['name'].append(name)
                d['linktype'].append(linktype)
                d['issue_id_1'].append(inwardIssue)
                d['issue_id_2'].append(outwardIssue)
            except Exception:
                logging.info("no epics")

            issuelinks = issue['fields']['issuelinks']

            for i in range(0, len(issuelinks)):
                issuelink = issuelinks[i]
                type = issuelink['type']
                linktype = type['name']
                try:
                    outwardIssue = issuelink['outwardIssue']['key']
                    inwardIssue = issue_key
                except Exception:
                    inwardIssue = issuelink['inwardIssue']['key']
                    outwardIssue = issue_key

                name = inwardIssue + "_" + outwardIssue

                d['name'].append(name)
                d['linktype'].append(linktype)
                d['issue_id_1'].append(inwardIssue)
                d['issue_id_2'].append(outwardIssue)

                logging.info("SUCCESS")

            issuest = issue['fields']['subtasks']

            for i in range(0, len(issuest)):
                issuesubtask = issuest[i]
                linktype = 'Subtask'
                outwardIssue = issuesubtask['key']
                inwardIssue = issue_key

                name = inwardIssue + "_" + outwardIssue

                d['name'].append(name)
                d['linktype'].append(linktype)
                d['issue_id_1'].append(inwardIssue)
                d['issue_id_2'].append(outwardIssue)

                logging.info("SUCCESS")
        except Exception as e:
            logging.info("!!ERROR!!ERROR!!ERROR!!ERROR!!ERROR!!ERROR!!ERROR!!")
            pass
    logging.info(f'Creating csv.')
    df = pd.DataFrame.from_dict(d)
    # adapt file path
    filename = '~data/raw/links_' + project.lower() + '.csv'
    df.to_csv(filename, sep=';', index=False)
    return None


def calculate_contributors(project):
    client = data_access.MongoDBConnection(host='localhost', port=27017,
                                           auth_mechanism=None, auth_source=None,
                                           password=None, username=None,
                                           connect_timeout=5000).client
    db = client['lynxdata']
    source_collection = db[project]
    cursor = source_collection.find({})

    user_set = set()
    creator_set = set()
    reporter_set = set()
    assignee_set = set()

    for issue in cursor:
        try:
            try:
                if project == 'JiraEcosystem':
                    issue_creator = issue['fields']['creator']['accountId']
                    creator_set.add(issue_creator)
                    user_set.add(issue_creator)

                else:
                    issue_creator = issue['fields']['creator']['key']
                    creator_set.add(issue_creator)
                    user_set.add(issue_creator)
            except:
                issue_creator = ''

            try:
                if project == 'JiraEcosystem':
                    issue_reporter = issue['fields']['reporter']['accountId']
                    reporter_set.add(issue_reporter)
                    user_set.add(issue_reporter)
                else:
                    issue_reporter = issue['fields']['reporter']['key']
                    reporter_set.add(issue_reporter)
                    user_set.add(issue_reporter)
            except:
                issue_reporter = ''

            try:
                if project == 'JiraEcosystem':
                    issue_assignee = issue['fields']['assignee']['accountId']
                    assignee_set.add(issue_assignee)
                    user_set.add(issue_assignee)
                else:
                    issue_assignee = issue['fields']['assignee']['key']
                    assignee_set.add(issue_assignee)
                    user_set.add(issue_assignee)
            except:
                issue_assignee = ''

        except Exception as e:
            logging.info("!!ERROR!!ERROR!!ERROR!!ERROR!!ERROR!!ERROR!!ERROR!!")
            pass

    logging.info(len(user_set))
    logging.info(len(creator_set))
    logging.info(len(reporter_set))
    logging.info(len(assignee_set))

    return [len(user_set), len(creator_set), len(reporter_set), len(assignee_set)]

def extract_link_history_authors(project):
    """
    Calculate the average number of comments per issue for Eclipse data.
    :return: The average values for all platforms.
    """
    client = data_access.MongoDBConnection(host='localhost', port=27017,
                                           auth_mechanism=None, auth_source=None,
                                           password=None, username=None,
                                           connect_timeout=5000).client
    db = client['lynxdata']
    source_collection = db[project]
    cursor = source_collection.find({})

    maintainer_set = set()
    for issue in cursor:
        try:
            issue_key = issue['key']

            history = issue['changelog']['histories']

            for i in range(0, len(history)):
                changes = history[i]['items']
                date = history[i]['created']
                for j in range(0, len(changes)):
                    typeOfChange = changes[j]['field']
                    if typeOfChange == 'Link':
                        try:
                            if project == 'JiraEcosystem':
                                maintainer = history[i]['author']['accountId']
                                maintainer_set.add(maintainer)
                            else:
                                maintainer = history[i]['author']['key']
                                maintainer_set.add(maintainer)
                        except:
                            maintainer = ''

        except Exception as e:
            logging.info("!!ERROR!!ERROR!!ERROR!!ERROR!!ERROR!!ERROR!!ERROR!!")
            pass
    logging.info(len(maintainer_set))

    return len(maintainer_set)

if __name__ == '__main__':
    # to_csv_with_changelog()
    # to_csv_with_changelog_items()
    # to_csv_with_links()
    # to_csv_orphans()
    #
    SOURCES = ['Apache', 'Hyperledger', 'IntelDAOS', 'JFrog', 'Jira',
               'JiraEcosystem',  'MariaDB', 'Mindville','Mojang' , 'MongoDB', 'Qt',
               'RedHat', 'Sakai', 'SecondLife', 'Sonatype', 'Spring']

    user_dict = {}

    for s in SOURCES:
        logging.info(s)
        extract_issue_csv(s)
        extract_links_csv(s)
        #

    # For Maintainer set:
    # for s in SOURCES:
    #     logging.info(s)
        # temp = extract_link_history_authors(s)
        # user_dict[s] = temp
    # logging.info(user_dict)
    # df = pd.DataFrame.from_dict(user_dict)
    # filename = '~/Desktop/maintainer_set.csv'
    #
    # logging.info(filename)
    # df.to_csv(filename, sep=';', index=False)

    # For User set:
    # for s in SOURCES:
    #     logging.info(s)
    #     temp = calculate_contributors(s)
    #     user_dict[s] = temp
    #
    # logging.info(user_dict)
    # df = pd.DataFrame.from_dict(user_dict)
    # filename = '~/Desktop/user_dict_je.csv'
    #
    # logging.info(filename)
    # df.to_csv(filename, sep=';', index=False)


