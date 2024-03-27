JSONexus
========

JSONexus is a lightweight and flexible database solution designed for modern applications. It provides a simple and intuitive way to store, query, and manipulate data using JSON documents.

Key Features
------------

*   Document-based storage
*   Flexible schema-less design
*   Powerful query capabilities
*   Easy integration with various platforms

Installation
------------

You can install JSONexus using pip:

    pip install jsonexus

Getting Started
---------------

Check out the [documentation](https://jsonexus.gitbook.io/jsonexus/) for detailed usage instructions, API reference, and examples.

Usage
-----

### Local Storage

```python
    from jsonexus import JSONexus
    
    # Create a local database
    db = JSONexus('data/db.json')
    
    # Insert a document
    db.insert('users', {'
    name': 'Alice', 
    'age': 30, 'email': 'alice@example.com'
    })
    
    # Find documents
    result = db.find('users', {'age': {'$gt': 25}})
    
    # Update a document
    db.update('users', {'name': 'Alice'}, {'age': 35})
    
    # Delete a document
    db.delete('users', {'name': 'Alice'})
    
    # Count documents
    count = db.count('users')
```
        

Documentation
-------------

The documentation for JSONexus can be found in the [Documentation](https://jsonexus.gitbook.io/jsonexus/) directory. It includes detailed usage instructions, API reference, and examples.

About
-----

JSONexus is an open-source project hosted on GitHub. You can contribute to the project, report issues, and request features on the GitHub repository

License
-------

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.