This Python tool makes it easy to back up Odoo databases and filestores. It helps create database backups, compress file stores, and send backups to remote servers using SFTP.

Once you install it, you'll find a configuration file in the /etc directory.(`/etc/db_backup.json`) You just need to edit this file and add your login details.

sample file

```
{
  "db_name": "Odoo Database Name",
  "db_user": "Odoo Database User Name",
  "db_password": "Database Password",
  "db_host": "localhost",
  "filestore_path": "~/.local/share/Odoo/filestore",
  "sftp_host": "SFTP server IP address or domain name",
  "sftp_port": 22,
  "sftp_username": "SFTP User Name",
  "sftp_password": "SFTP Password",
  "sftp_directory": "~/Videos/odoo_backup/"
}
```

here you need to change the values of db_name, db_user, db_password, db_host, filestore_path, sftp_host, sftp_port, sftp_username, sftp_password, sftp_directory.   
