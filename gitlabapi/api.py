import requests
import json


class GitlabApi(object):
    def __init__(self, api_key, project_url):
        try:
            self.api_key = api_key.strip('\n\r')
            self.api_url = self._get_project_api_url(project_url)
            self.project_id = self._get_project_id(project_url)
        except Exception as error:
            print('Did not manage to instantiate GitlabApi have you set you key?')

    def _get_query(self, url_append, project=True):
        if hasattr(self, 'project_id') and project:
            url_append = 'projects/' + str(self.project_id) + '/' + url_append
        data = requests.get(self.api_url + '/' + url_append, headers={'PRIVATE-TOKEN': self.api_key})
        return data.json()

    def _post_query(self, url_append, params):
        data = requests.post(self.api_url + '/projects/' + str(self.project_id) + '/' + url_append, params, headers={'PRIVATE-TOKEN': self.api_key})
        return data.json()

    def _put_query(self, url_append, params):
        data = requests.put(self.api_url + '/projects/' + str(self.project_id) + '/' + url_append, params, headers={'PRIVATE-TOKEN': self.api_key})
        return data.json()

    def _get_project_api_url(self, project_url):
        host = str(project_url).split('/')[2]
        if ':' in host:
            host = host.split(':')[0]
        if '@' in host:
            host = host.split('@')[1]
        return 'http://' + host + '/api/v4'

    def _get_project_id(self, project_url):
        return [project['id'] for project in self._get_query('projects?per_page=300') if project['ssh_url_to_repo'] == project_url or project['http_url_to_repo'] == project_url][0]

    def _create_mr(self, name, source, destination, description=None):
        params = {
            'source_branch': source,
            'target_branch': destination,
            'title': name
        }
        if description is not None:
            params['description'] = description
        return self._post_query('merge_requests', params)

    def _create_issue(self, name, description):
        params = {
            'title': name
        }
        if description is not None:
            params['description'] = description
        return self._post_query('issues', params)

    def _get_user_id(self, name):
        return [user['id'] for user in self._get_query('users?per_page=300', False) if user['username'] == name][0]

    def _assign(self, name, iid, mr=True):
        user_id = self._get_user_id(name)
        if mr:
            what = 'merge_requests'
            params = {'assignee_id': user_id}
        else:
            what = 'issues'
            params = {'assignee_ids': [user_id]}
        return self._put_query(what + '/' + str(iid), params)

    def create_mr(self, **kwargs):
        mr = self._create_mr(kwargs['name'], kwargs['source'], kwargs['destination'], kwargs['description'])
        if kwargs['assign']:
            self._assign(kwargs['assign'], mr['iid'])

    def create_issue(self, **kwargs):
        issue = self._create_issue(kwargs['name'], kwargs['description'])
        if kwargs['assign']:
            self._assign(kwargs['assign'], issue['iid'], False)


