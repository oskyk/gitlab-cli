import requests
import json


class GitlabApi(object):
    def __init__(self, api_key, project_url):
        self.api_key = api_key
        self.api_url = self._get_project_api_url(project_url)
        self.project_id = self._get_project_id(project_url)

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

    def _get_user_id(self, name):
        return [user['id'] for user in self._get_query('users?per_page=300', False) if user['username'] == name][0]

    def _assign(self, name, iid, what='merge_requests'):
        user_id = self._get_user_id(name)
        return self._put_query(what + '/' + str(iid), {'assignee_id': user_id})

    def create_mr(self, **kwargs):
        mr = self._create_mr(kwargs['name'], kwargs['source'], kwargs['destination'], kwargs['description'])
        if kwargs['assign']:
            self._assign(kwargs['assign'], mr['iid'])

