##############################################################################
# Halo API remove empty groups from your portal
# Author: Sean Nicholson
# Version 1.0.0
# Date 07.24.2018
# v 1.0.0 - initial release
##############################################################################


import cloudpassage, yaml, time



def create_api_session(session):
    config_file_loc = "cloudpassage.yml"
    config_info = cloudpassage.ApiKeyManager(config_file=config_file_loc)
    session = cloudpassage.HaloSession(config_info.key_id, config_info.secret_key)
    return session


def remove_groups(session):
    groups_deleted = []
    super_count = 1
    while super_count > 0:
        count = 0
        api_results_list = cloudpassage.HttpHelper(session)
        list_of_groups = api_results_list.get_paginated("/v1/groups?per_page=1000", "groups", 20)
        #print list_of_groups
        for group in list_of_groups:
            if group['server_counts']['active'] == 0 and group['has_children'] == False and group['parent_id']:
                query_url = "/v1/groups/" + group['id']
                #print "found one"
                api_results_list.delete(query_url)
                groups_deleted.append({'group name': group['name'],'group path': group['group_path'],'group ID': group['id']})
                count += 1
        time.sleep(30) #wait for API to update
        if count == 0:
            super_count = 0
    if len(groups_deleted) > 0:
        print groups_deleted
        print "\nScript results: {0} groups deleted\n".format(str(len(groups_deleted)))
    else:
        print "No groups deleted... Please move active servers from groups to be deleted"


if __name__ == "__main__":
    api_session = None
    api_session = create_api_session(api_session)
    remove_groups(api_session)
