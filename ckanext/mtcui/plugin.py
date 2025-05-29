import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.config.declaration import Declaration, Key

import ckanext.mtcui.views as views
from ckanext.mtcui.logic import (
    action, auth, validators
)
import ckanext.mtcui.helpers as helpers  # ตรวจสอบให้แน่ใจว่านำเข้า helpers


# import ckanext.mtcui.cli as cli
# import ckanext.mtcui.helpers as helpers
# import ckanext.mtcui.views as views
# from ckanext.mtcui.logic import (
#     action, auth, validators
# )


class MtcuiPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IAuthFunctions)
    plugins.implements(plugins.IActions)
    plugins.implements(plugins.IBlueprint)
    plugins.implements(plugins.ITemplateHelpers)




    def update_config(self, config_):
        toolkit.add_template_directory(config_, "templates")
        toolkit.add_public_directory(config_, "public")
        toolkit.add_resource("assets", "mtcui")
  

        config_['ckan.base_public_folder'] = 'public'
        config_['ckan.extra_public_paths'] = 'public'


    # IAuthFunctions
    def get_auth_functions(self):
        return auth.get_auth_functions()

    # IActions
    def get_actions(self):
        return action.get_actions()

    # IBlueprint
    def get_blueprint(self):
        return views.get_blueprint()

    # ITemplateHelpers
    def get_helpers(self):
        return helpers.get_helpers()

    # IClick

    # def get_commands(self):
    #     return cli.get_commands()

    # IValidators

    # def get_validators(self):
    #     return validators.get_validators()
    
   
