# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

# Note: Do not add new arguments to setup(), instead add setuptools
# configuration options to setup.cfg, or any other project information
# to pyproject.toml
# See https://github.com/ckan/ckan/issues/8382 for details

setup(
    name='ckanext-mtcui',
    version='0.1.0',
    description='CKAN의 사용자 인터페이스를 개선하기 위한 확장 모듈',
    long_description='''
    CKAN의 사용자 인터페이스를 개선하기 위한 확장 모듈입니다.
    메인 페이지 커스터마이징, 데이터셋 페이지 개선, 네비게이션 메뉴 추가 등의 기능을 제공합니다.
    ''',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    keywords='ckan, ui, extension',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/your-org/ckanext-mtcui',
    license='MIT',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    namespace_packages=['ckanext'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'ckan==2.11.2',
    ],
    entry_points='''
        [ckan.plugins]
        mtcui=ckanext.mtcui.plugin:MtcuiPlugin
    ''',
    # If you are changing from the default layout of your extension, you may
    # have to change the message extractors, you can read more about babel
    # message extraction at
    # http://babel.pocoo.org/docs/messages/#extraction-method-mapping-and-configuration
    message_extractors={
        'ckanext': [
            ('**.py', 'python', None),
            ('**.js', 'javascript', None),
            ('**/templates/**.html', 'ckan', None),
        ],
    }
)
