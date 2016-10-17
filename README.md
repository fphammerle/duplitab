# duplitab
wrapper for duplicity featuring persistent backup configuration

## Configuration

```yaml
# /etc/duplitab
-   source_path: /home
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
$ duplitab -filter-target-url '.*media/backup/[hs].*' list --table-style tabular
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
$ duplitab -filter-target-url '.*media/backup/[hs].*' backup
```
