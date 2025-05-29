import ckan.plugins.toolkit as tk
import ckanext.mtcui.logic.schema as schema


@tk.side_effect_free
def mtcui_get_sum(context, data_dict):
    tk.check_access(
        "mtcui_get_sum", context, data_dict)
    data, errors = tk.navl_validate(
        data_dict, schema.mtcui_get_sum(), context)

    if errors:
        raise tk.ValidationError(errors)

    return {
        "left": data["left"],
        "right": data["right"],
        "sum": data["left"] + data["right"]
    }


def get_actions():
    return {
        'mtcui_get_sum': mtcui_get_sum,
    }
