# General configurations for wordpress-workflow
SITE_CONFIG = {
    'version': '3.9.1',
    'locale': 'es_ES',

    'dev': {
        'url': 'wordpress-workflow.local',
        'title': 'New Project',
        #Admin config
        'admin_user': 'admin',
        'admin_password': 'password',
        'admin_email': 'admin@email.com',
        #database config 
        'dbname': 'wordpress_workflow',
        'dbuser': 'root',
        'dbpassword': 'password',
        'dbhost': 'localhost'
    }
}
