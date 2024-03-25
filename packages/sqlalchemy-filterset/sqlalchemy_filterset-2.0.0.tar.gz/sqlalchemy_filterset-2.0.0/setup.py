# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sqlalchemy_filterset']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy[asyncio]>=2,<3']

setup_kwargs = {
    'name': 'sqlalchemy-filterset',
    'version': '2.0.0',
    'description': 'An easy way to filter, sort, paginate SQLAlchemy queries',
    'long_description': '<h1>\n  <span style="font-size: 65px; color: #7e56c2; font-weight: 600">\n    <strong>SQLAlchemy Filterset</strong>\n  </span>\n</h1>\n\n<p align="left">\n    <em>An easy way to filter, sort, paginate SQLAlchemy queries</em>\n</p>\n\n[![codecov](https://codecov.io/gh/sqlalchemy-filterset/sqlalchemy-filterset/branch/main/graph/badge.svg)](https://codecov.io/gh/sqlalchemy-filterset/sqlalchemy-filterset)\n[![PyPI version](https://badge.fury.io/py/sqlalchemy-filterset.svg)](https://badge.fury.io/py/sqlalchemy-filterset)\n[![Downloads](https://pepy.tech/badge/sqlalchemy-filterset)](https://pepy.tech/project/sqlalchemy-filterset)\n[![CodeQL](https://github.com/sqlalchemy-filterset/sqlalchemy-filterset/actions/workflows/codeql.yml/badge.svg)](https://github.com/sqlalchemy-filterset/sqlalchemy-filterset/actions/workflows/codeql.yml)\n\n\n<img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/sqlalchemy-filterset?color=%2334D058">\n<img alt="SqlAlchemy - Version" src="https://img.shields.io/badge/sqlalchemy-2.0+-%2334D058">\n\n---\n**Documentation**: <a href="https://sqlalchemy-filterset.github.io/sqlalchemy-filterset/" target="_blank">https://sqlalchemy-filterset.github.io/sqlalchemy-filterset</a>\n\n**Source Code**: <a href="https://github.com/sqlalchemy-filterset/sqlalchemy-filterset" target="_blank">https://github.com/sqlalchemy-filterset/sqlalchemy-filterset</a>\n\n---\nThe library provides a convenient and organized way to filter your database records.\nBy creating a `FilterSet` class, you can declaratively define the filters you want to apply to your `SQLAlchemy` queries.\nThis library is particularly useful in web applications, as it allows users to easily search, filter, sort, and paginate data.\n\nThe key features are:\n\n* [X] Declarative definition of filters.\n* [X] Keeping all of your filters in one place, making it easier to maintain and change them as needed.\n* [X] Constructing complex filtering conditions by combining multiple simple filters.\n* [X] Offer of a standard approach to writing database queries.\n* [X] Reduction of code duplication by reusing the same filters in multiple places in your code.\n* [X] Sync and Async support of modern SQLAlchemy.\n\n## Installation\n\n```bash\npip install sqlalchemy-filterset\n```\nRequirements: `Python 3.7+` `SQLAlchemy 2.0+`\n\n\n## Basic FilterSet and Filters Usage\n\nIn this example we specify criteria for filtering the database records\nby simply setting the attributes of the `ProductFilterSet` class.\nThis is more convenient and easier to understand than writing raw SQL queries, which\ncan be more error-prone and difficult to maintain.\n\n### Define a FilterSet\n\n```python\nfrom sqlalchemy_filterset import BaseFilterSet, Filter, RangeFilter, BooleanFilter\n\nfrom myapp.models import Product\n\n\nclass ProductFilterSet(BaseFilterSet):\n    id = Filter(Product.id)\n    price = RangeFilter(Product.price)\n    is_active = BooleanFilter(Product.is_active)\n```\n### Define a FilterSchema\n```python\nimport uuid\nfrom pydantic import BaseModel\n\n\nclass ProductFilterSchema(BaseModel):\n    id: uuid.UUID | None\n    price: tuple[float, float] | None\n    is_active: bool | None\n```\n\n### Usage\n```python\n# Connect to the database\nengine = create_engine("postgresql://user:password@host/database")\nBase.metadata.create_all(bind=engine)\nSessionLocal = sessionmaker(bind=engine)\nsession = SessionLocal()\n\n# Define sqlalchemy query\nquery = select(Product)\n\n# Define parameters for filtering\nfilter_params = ProductFilterSchema(price=(10, 100), is_active=True)\n\n# Create the filterset object\nfilter_set = ProductFilterSet(query)\n\n# Apply the filters to the query\nquery = filter_set.filter_query(filter_params.dict(exclude_unset=True))\n\n# Execute the query\nsession.execute(query).unique().scalars().all()\n```\n\nThis example will generate the following query:\n```sql\nselect product.id, product.title, product.price, product.is_active\nfrom product\nwhere product.price >= 10\n  and product.price <= 100\n  and product.is_active = true;\n```\n\n\n## License\n\nThis project is licensed under the terms of the MIT license.\n\n\n## Supported by\n<a href="https://idaproject.com/" target="_blank" title="idaproject"><img width=150 src="https://sqlalchemy-filterset.github.io/sqlalchemy-filterset/img/idaproject.png"></a>\n',
    'author': 'Andrey Matveev',
    'author_email': 'ra1ze.matveev@yandex.ru',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0.0',
}


setup(**setup_kwargs)
