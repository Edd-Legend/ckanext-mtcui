import ckan.plugins.toolkit as tk


@tk.auth_allow_anonymous_access
def mtcui_get_sum(context, data_dict):
    return {"success": True}


def get_auth_functions():
    return {
        "mtcui_get_sum": mtcui_get_sum,
    }
