# duplitab
wrapper for duplicity featuring persistent backup configuration

## Configuration

```yaml
# /etc/duplitab
-   name: home at media backup
    source_path: /home
    target_url: file:///media/backup/home
    encryption: no
-   source_path: /secret/folder
    target_url: sftp://user@server//media/backup/secret
    encrypt_key: ABCDEFGH # gnupg
    # target_via_sshfs: true
-   source_path: /var/www
    target_url: file:///media/backup/web
    selectors:
    -   option: exclude
        shell_pattern: '**/cache'
    -   option: include
        shell_pattern: /var/www/src
    -   option: exclude
        shell_pattern: '**'
    encryption: no
```

## Show Configuration

```bash
$ duplitab list --table-style tabular
source type      source host  source path     target url                               encrypt key
-------------  -------------  --------------  ---------------------------------------  -------------
local                         /home           file:///media/backup/home
local                         /secret/folder  sftp://user@server//media/backup/secret  ABCDEFGH
local                         /var/www        file:///media/backup/web
```
```bash
$ duplitab --filter-target-url '.*media/backup/[hs].*' list --table-style tabular
source type      source host  source path     target url                               encrypt key
-------------  -------------  --------------  ---------------------------------------  -------------
local                         /home           file:///media/backup/home
local                         /secret/folder  sftp://user@server//media/backup/secret  ABCDEFGH
```

## Backup

```bash
$ duplitab backup
```
```bash
$ duplitab --filter-target-url '.*media/backup/[hs].*' backup
```

## Show Status

```bash
$ duplitab --filter-target-url '.*media/backup/[hs].*' status --table-style tabular
target url                               last_backup
---------------------------------------  -------------------
file:///media/backup/home                2016-10-23 08:35:13
sftp://user@server//media/backup/secret  2016-09-22 09:36:14
```
