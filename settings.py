# General configurations for wordpress-workflow
SITE_CONFIG = {
    'version': '3.9.1',
    'locale': 'es_ES',
    'theme': 'yourtheme',

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
# 3rd party plugins

PLUGINS_CONFIG = (
    {
        'name': 'wordpress-seo',
        'active': True,
        'version': 'stable'
    },
    {
        'name': 'contact-form-7',
        'active': True,
        'version': 'stable'
    },
    {
        'name': 'wp-super-cache',
        'active': True,
        'version': 'stable'
    },
)

# Own plugins
CUSTOM_PLUGINS_CONFIG = (
    {
        'name': 'jetpack',
        'active': True
    },
)
