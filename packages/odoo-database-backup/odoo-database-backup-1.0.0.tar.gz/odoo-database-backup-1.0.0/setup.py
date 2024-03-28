from setuptools import setup, find_packages
import os

# Define the path to the configuration file
etc_dir = '/etc'
config_file = 'db_backup.json'

# Create a list of (target directory, source files) tuples
data_files = [(etc_dir, [config_file])]

# Ensure that the target directory exists
if not os.path.exists(etc_dir):
    os.makedirs(etc_dir)

setup(
    name='odoo-database-backup',
    version='1.0.0',
    description='This Python package designed to simplify and automate the process of backing up Odoo databases and filestores. With this package, you can easily create database backups, compress filestores, and transfer the backups to remote servers via SFTP.',
    author='Pragmatic: Sagar',
    packages=find_packages(),
    install_requires=['paramiko', 'psycopg2-binary'],
    data_files=data_files
)

