from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

setup(name='prisma_sdwan_config',
      version='0.0.7',
      description='Configuration exporting and Continuous Integration (CI) capable configuration importing for the '
                  'Prisma Sase Cloud Controller.',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/glspi/prisma_sdwan_config',
      author='CloudGenix Developer Support - build_site by glspi',
      author_email='',
      license='MIT',
      include_package_data=True,
      install_requires=[
            'cloudgenix >= 6.1.1b1, < 6.1.3b1',
            'PyYAML >= 5.3',
            'jinja2==3.1.2',
            'typer==0.7.0',
            'prisma_sase @ git+https://github.com/PaloAltoNetworks/prisma-sase-sdk-python.git'
      ],
      packages=['cloudgenix_config', 'yaml_config'],
      entry_points={
            'console_scripts': [
                  'do_site = cloudgenix_config.do:go',
                  'pull_site = cloudgenix_config.pull:go',
                  'build_site = yaml_config.build:go'
                  ]
      },
      classifiers=[
            "Development Status :: 4 - Beta",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.11"
      ]
      )
