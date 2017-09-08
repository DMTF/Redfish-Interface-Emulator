from setuptools import setup

setup(name='redfish-interface-emulator',
      version='1.0.0',
      description='The Redfish Interface Emulator that can emulator a Redfish interface resources as static or dynamically',
      author='DMTF, https://www.dmtf.org/standards/feedback',
      license='BSD 3-clause "New" or "Revised License"',
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'License :: OSI Approved :: BSD License',
          'Programming Language :: Python :: 3.5',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: Communications'
      ],
      keywords='Redfish',
      url='https://github.com/DMTF/Redfish-Interface-Emulator',
      download_url='https://github.com/DMTF/Redfish-Interface-Emulator/archive/1.0.0.tar.gz',
      packages=['redfish-interface-emulator'],
      scripts=['scripts/redfish-interface-emulator','scripts/redfish-interface-emulator-ssl'],
      install_requires=['Flask','aniso8601','itsdangerous','Jinja2','MarkupSafe','pytz','requests','six','Werkzeug','StringGenerator','flask_restful','urllib3','flash_httpauth']
)
