from __future__ import annotations
from typing import Any, Optional

import jinja2
import datetime
from markupsafe import Markup
import logging
import ckan.plugins.toolkit as tk
from sqlalchemy.sql import text
from ckan.lib.helpers import url_for_static
from ckan.model import Package, Session, Resource
from ckan.model.meta import Session
from sqlalchemy import func, text
import random
    
from ckan.types import Context

from . import changes

log = logging.getLogger(__name__)


def dashboard_activity_stream(
    user_id: str,
    filter_type: Optional[str] = None,
    filter_id: Optional[str] = None,
    offset: int = 0,
    limit: int = 0,
    before: Optional[datetime.datetime] = None,
    after: Optional[datetime.datetime] = None,
) -> list[dict[str, Any]]:
    """Return the dashboard activity stream of the current user.

    :param user_id: the id of the user
    :type user_id: string

    :param filter_type: the type of thing to filter by
    :type filter_type: string

    :param filter_id: the id of item to filter by
    :type filter_id: string

    :returns: an activity stream as an HTML snippet
    :rtype: string

    """
    context: Context = {"user": tk.g.user}
    if filter_type:
        action_functions = {
            "dataset": "package_activity_list",
            "user": "user_activity_list",
            "group": "group_activity_list",
            "organization": "organization_activity_list",
        }
        action_function = tk.get_action(action_functions[filter_type])
        return action_function(
            context, {
                "id": filter_id,
                "limit": limit,
                "offset": offset,
                "before": before,
                "after": after
                })
    else:
        return tk.get_action("dashboard_activity_list")(
            context, {
                "offset": offset,
                "limit": limit,
                "before": before,
                "after": after
                }
        )


def recently_changed_packages_activity_stream(limit: Optional[int] = 100) -> list[dict[str, Any]]:
    context = {"user": tk.g.user or ''}
    data_dict = {
        "sort": "metadata_modified desc",
        "rows": limit,
        "fq": "dataset_type:dataset"
    }
    result = tk.get_action("package_search")(context, data_dict)
    return result["results"]



def activity_show_email_notifications() -> bool:
    return tk.config.get("ckan.activity_streams_email_notifications")
def get_all_resources(limit=100):
    """
    Get a list of resources from the database.
    
    Args:
        limit (int): Maximum number of resources to return
        
    Returns:
        list: List of resource dictionaries
    """
    resources = Session.query(Resource).filter(Resource.state == 'active').limit(limit).all()
    return resources
    
def get_all_resources1(limit=100):
    """
    Return top N most downloaded resources based on tracking_raw logs.
    
    Args:
        limit (int): Number of top downloaded resources to return
    
    Returns:
        list of dict: Each dict contains resource fields and download_count
    """
    sql = text("""
        SELECT 
            r.id AS id,
            r.name AS name,
            r.url AS url,
            r.format AS format,
            r.package_id AS package_id,
            COUNT(tr.url) AS download_count
        FROM resource r
        LEFT JOIN tracking_raw tr
            ON tr.tracking_type = 'resource'
            AND tr.url LIKE CONCAT('%/resource/', r.id, '/download/%')
        WHERE r.state = 'active'
        GROUP BY r.id, r.name, r.url, r.format, r.package_id
        ORDER BY download_count DESC
        LIMIT :limit
    """)
    result = Session.execute(sql, {'limit': limit})
    return [dict(row) for row in result]

def mtcui_hello():
    return "Hello, mtcui!"

def most_popular_groups():
    '''Return a sorted list of the groups with the most datasets.'''
    # Get a list of all the site's groups from CKAN, sorted by number of
    # datasets.
    groups = tk.get_action('group_list')(
        {}, {'sort': 'package_count desc', 'all_fields': True})
    # Truncate the list to the 10 most popular groups only.
    groups = groups[:10]
    return groups


def mtcui_get_packages(limit=5):
    package_list = tk.get_action('package_list')(
        context={}, data_dict={'limit': limit}
    )
    packages = []
    for pkg_name in package_list:
        pkg = tk.get_action('package_show')(
            context={}, data_dict={'id': pkg_name}
        )
        packages.append(pkg)
    return packages

def group_list():
    '''Return a list of all groups.'''
    context = {'ignore_auth': True}
    data_dict = {'all_fields': True}
    return tk.get_action('group_list')(context, data_dict)

def get_dataset_count():
    '''Return the total number of datasets.'''
    context = {'ignore_auth': True}
    data_dict = {
        'rows': 0,  # We don't need the actual results, just the count
        'fq': 'dataset_type:dataset',
        'include_private': False
    }
    result = tk.get_action('package_search')(context, data_dict)
    return result.get('count', 0)

def get_dataset_count1():
    '''Return the total number of datasets.'''
    context = {'ignore_auth': True}
    data_dict = {
        'rows': 0,  # We don't need the actual results, just the count
        'fq': 'dataset_type:dataset',
        'include_private': True
    }
    result = tk.get_action('package_search')(context, data_dict)
    return result.get('count', 0)

def get_resource_count():
    context = {'ignore_auth': True}
    data_dict = {
        'rows': 1000,  # ดึงครั้งละ 1000 ชุด
        'fq': 'dataset_type:dataset',
        'include_private': True,
        'start': 0  # เริ่มจากชุดข้อมูลแรก
    }
    total_resources = 0
    
    while True:
        result = tk.get_action('package_search')(context, data_dict)
        datasets = result.get('results', [])
        if not datasets:  # ถ้าไม่มี Datasets เพิ่มแล้ว ให้หยุด
            break
        for dataset in datasets:
            resources = dataset.get('resources', [])
            total_resources += len(resources)
        data_dict['start'] += data_dict['rows']  # ขยับไปหน้าถัดไป
    
    return total_resources
def get_organization_count():
    '''Return the total number of organizations (bureaus).'''
    context = {'ignore_auth': True}
    data_dict = {'all_fields': True}
    return len(tk.get_action('organization_list')(context, data_dict))

def get_economy_dataset_count():
    '''Return the number of datasets tagged with economy.'''
    context = {'ignore_auth': True}
    data_dict = {
        'rows': 1000,  # Get 1000 datasets at a time
        'fq': 'dataset_type:dataset AND tags:economy',  # Filter for economy tag
        'include_private': True,
        'start': 0  # Start from first dataset
    }
    total_datasets = 0
    
    while True:
        result = tk.get_action('package_search')(context, data_dict)
        datasets = result.get('results', [])
        if not datasets:  # If no more datasets, stop
            break
        total_datasets += len(datasets)
        data_dict['start'] += data_dict['rows']  # Move to next page
    
    return total_datasets

def get_education_dataset_count():
    '''Return the number of datasets tagged with education.'''
    context = {'ignore_auth': True}
    data_dict = {
        'rows': 1000,  # Get 1000 datasets at a time
        'fq': 'dataset_type:dataset AND tags:education',  # Filter for economy tag
        'include_private': True,
        'start': 0  # Start from first dataset
    }
    total_datasets = 0
    
    while True:
        result = tk.get_action('package_search')(context, data_dict)
        datasets = result.get('results', [])
        if not datasets:  # If no more datasets, stop
            break
        total_datasets += len(datasets)
        data_dict['start'] += data_dict['rows']  # Move to next page
    
    return total_datasets

def get_most_visited_datasets(limit=6):
    sql = text("""
        SELECT package_id, SUM(running_total) AS total_views
        FROM tracking_summary
        WHERE tracking_type = 'page'
        GROUP BY package_id
        ORDER BY total_views DESC
        LIMIT :limit
    """)
    result = Session.execute(sql, {'limit': limit}).fetchall()

    datasets = []
    for row in result:
        try:
            pkg = tk.get_action('package_show')({}, {'id': row.package_id})
            pkg['total_views'] = row.total_views
            datasets.append(pkg)
        except:
            continue  # skip dataset not found (e.g., deleted)
    return datasets


def get_organizations():
    """Get all organizations."""
    return tk.get_action('organization_list')({}, {'all_fields': True})

def get_bureaus():
    """Get all bureau-level organizations."""
    orgs = tk.get_action('organization_list')({}, {'all_fields': True})
    return [org for org in orgs if org.get('type') == 'bureau']

def get_groups():
    """Get all groups with dataset counts."""
    groups = tk.get_action('group_list')({}, {'all_fields': True})
    return groups

def get_formats():
    """Get all unique formats used in datasets with counts."""
    formats = {}
    datasets = tk.get_action('package_list')({}, {'limit': 1000})
    
    for dataset in datasets:
        package = tk.get_action('package_show')({}, {'id': dataset})
        for resource in package.get('resources', []):
            format = resource.get('format', '').upper()
            if format:
                formats[format] = formats.get(format, 0) + 1
    
    return [{'name': name, 'count': count} for name, count in formats.items()]

def get_group_color(group_name):
    """Generate a consistent color for a group."""
    colors = [
        '#c30082',  # Pink
        '#ad9ea8',  # Gray
        '#18a1c4',  # Blue
        '#2c3e50',  # Dark Blue
        '#27ae60',  # Green
        '#f39c12',  # Orange
        '#8e44ad',  # Purple
        '#c0392b',  # Red
    ]
    # Use the group name to consistently select a color
    index = sum(ord(c) for c in group_name) % len(colors)
    return colors[index]

def get_organization_datasets(org_id):
    """Get all datasets for an organization."""
    return tk.get_action('organization_show')({}, {'id': org_id, 'include_datasets': True})

def get_organization(org_id):
    """Get organization details by ID."""
    return tk.get_action('organization_show')({}, {'id': org_id})

def get_download_count_for_dataset(dataset_name):
    dataset_id = tk.get_action('package_show')({}, {'id': dataset_name})['id']
    sql = text("""
        SELECT COUNT(*) 
        FROM tracking_raw
        WHERE tracking_type = 'resource'
        AND url LIKE :pattern
    """)
    pattern = f'%dataset/{dataset_id}/resource/%/download/%'
    result = Session.execute(sql, {'pattern': pattern}).fetchone()
    return result[0] or 0

def get_download_count_for_dataset_summary_using_url(dataset_name):
    dataset_id = tk.get_action('package_show')({}, {'id': dataset_name})['id']
    sql = text("""
        SELECT COUNT(*) 
        FROM tracking_summary
        WHERE tracking_type = 'resource'
        AND url LIKE :pattern
    """)
    pattern = f'%dataset/{dataset_id}/resource/%/download/%'
    result = Session.execute(sql, {'pattern': pattern}).fetchone()
    return result[0] or 0

def get_download_count_for_dataset_summary(dataset_name):
    # ใช้ action เพื่อหาค่า dataset id จากชื่อ
    dataset_id = tk.get_action('package_show')({}, {'id': dataset_name})['id']
    
    # SQL สรุปยอดดาวน์โหลดจาก tracking_summary
    sql = text("""
        SELECT SUM(count) AS download_count
        FROM tracking_summary
        WHERE package_id = :package_id
          AND tracking_type = 'resource'
    """)
    
    result = Session.execute(sql, {'package_id': dataset_id}).fetchone()
    return result.download_count or 0

def get_download_count_from_summary_for_resource(resource_id: str) -> int:
    sql = text("""
        SELECT SUM(count) AS download_count
        FROM tracking_summary
        WHERE tracking_type = 'resource'
          AND url LIKE :pattern
    """)
    pattern = f'%/resource/{resource_id}/download/%'
    result = Session.execute(sql, {'pattern': pattern}).fetchone()
    return result.download_count or 0

def get_download_count_for_resource(resource_id: str) -> int:
    sql = text("""
        SELECT COUNT(*) 
        FROM tracking_raw
        WHERE tracking_type = 'resource'
          AND url LIKE :pattern
    """)
    pattern = f'%/resource/{resource_id}/download/%'
    result = Session.execute(sql, {'pattern': pattern}).fetchone()
    return result[0] or 0



def get_view_count_for_dataset(dataset_name):
    dataset_id = tk.get_action('package_show')({}, {'id': dataset_name})['id']
    sql = text("""
        SELECT SUM(running_total) AS total_views
        FROM tracking_summary
        WHERE tracking_type = 'page'
        AND package_id = :package_id
    """)
    result = Session.execute(sql, {'package_id': dataset_id}).fetchone()
    return result.total_views or 0

def get_view_count_for_dataset_raw(dataset_name):
    dataset_id = tk.get_action('package_show')({}, {'id': dataset_name})['id']
    
    sql = text("""
        SELECT COUNT(*) AS total_views
        FROM tracking_raw
        WHERE tracking_type = 'page'
          AND url LIKE :pattern
    """)
    
    pattern = f'%/dataset/{dataset_id}%'
    result = Session.execute(sql, {'pattern': pattern}).fetchone()
    
    return result.total_views or 0

def get_recent_view_count_for_dataset(dataset_id: str, days: int = 1) -> int:
    sql = text("""
        SELECT SUM(recent_views)
        FROM tracking_summary
        WHERE package_id = :dataset_id
          AND tracking_type = 'page'
          AND tracking_date >= CURRENT_DATE - INTERVAL :days
    """)
    result = Session.execute(sql, {'dataset_id': dataset_id, 'days': f'{days} days'}).fetchone()
    return result[0] or 0

def get_recent_view_count_for_dataset_raw(dataset_id: str, days: int = 1) -> int:
    sql = text("""
        SELECT COUNT(*) 
        FROM tracking_raw
        WHERE tracking_type = 'page'
          AND url LIKE :pattern
          AND tracking_date >= CURRENT_DATE - INTERVAL :interval
    """)
    
    pattern = f'%/dataset/{dataset_id}%'
    interval = f'{days} days'
    
    result = Session.execute(sql, {'pattern': pattern, 'interval': interval}).fetchone()
    return result[0] or 0


def get_helpers():
    return {
        "mtcui_hello": mtcui_hello,
        "activity_show_email_notifications": activity_show_email_notifications,
        "recently_changed_packages_activity_stream": recently_changed_packages_activity_stream,
        "dashboard_activity_stream": dashboard_activity_stream,
        "most_popular_groups": most_popular_groups,
        "mtcui_get_packages": mtcui_get_packages,
        "group_list": group_list,
        "get_dataset_count": get_dataset_count,
        "get_dataset_count1": get_dataset_count1,
        "get_resource_count": get_resource_count,
        "get_organization_count": get_organization_count,
        "get_economy_dataset_count": get_economy_dataset_count,
        "get_education_dataset_count": get_education_dataset_count,
        "get_most_visited_datasets": get_most_visited_datasets,
        "get_organizations": get_organizations,
        "get_bureaus": get_bureaus,
        "get_groups": get_groups,
        "get_formats": get_formats,
        "get_group_color": get_group_color,
        "get_organization_datasets": get_organization_datasets,
        "get_organization": get_organization,
        'get_download_count_for_dataset': get_download_count_for_dataset,
        'get_download_count_for_dataset_summary': get_download_count_for_dataset_summary,
        'get_download_count_for_dataset_summary_using_url': get_download_count_for_dataset_summary_using_url,
        'get_download_count_from_summary_for_resource': get_download_count_from_summary_for_resource,
        'get_download_count_for_resource': get_download_count_for_resource,
        'get_view_count_for_dataset': get_view_count_for_dataset,
        'get_view_count_for_dataset_raw': get_view_count_for_dataset_raw,
        'get_recent_view_count_for_dataset': get_recent_view_count_for_dataset,
        'get_recent_view_count_for_dataset_raw': get_recent_view_count_for_dataset_raw,
        "get_all_resources1": get_all_resources1,
        "get_all_resources": get_all_resources,
    }

