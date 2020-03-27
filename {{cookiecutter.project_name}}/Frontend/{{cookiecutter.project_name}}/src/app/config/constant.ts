export const domainConfig={
	client : '{{cookiecutter.project_name}}',
	virtual_host:'{{cookiecutter.domain_name}}',
	domainApp : '{{cookiecutter.domain_name}}',
	staticStorage:"static/storage/"
}
export const oAuthConfig={
	client_id : '',
	client_secret: '',
	username: 'appmobile',
	password: '{{cookiecutter.project_name}}'
}
export const GOOGLE_MAP_API_KEY=""
