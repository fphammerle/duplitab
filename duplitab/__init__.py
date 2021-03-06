import datetime
import re
import subprocess
import sys
import time


class DuplicityCommandFailedError(RuntimeError):

    @property
    def msg(self):
        return self.__cause__.output.decode(sys.stdout.encoding)


def _duplicity(params, timeout_seconds=None):
    try:
        stdout = subprocess.check_output(
            ['duplicity']
            + (['--timeout', str(timeout_seconds)] if timeout_seconds else [])
            + params,
            stderr=subprocess.STDOUT,
        )
    except subprocess.CalledProcessError as ex:
        raise DuplicityCommandFailedError() from ex
    return stdout.decode(sys.stdout.encoding)


def _parse_duplicity_timestamp(timestamp):
    return datetime.datetime.fromtimestamp(
        time.mktime(time.strptime(timestamp))
    )


class Collection(object):

    def __init__(self, url):
        self.url = url

    def request_status(self, timeout_seconds=None):
        return _CollectionStatus._parse(
            text=_duplicity(
                ['collection-status', self.url],
                timeout_seconds=timeout_seconds,
            )
        )


class _Status(object):

    def __eq__(self, other):
        return isinstance(self, type(other)) and vars(self) == vars(other)

    def __neq__(self, other):
        return not (self == other)


class _CollectionStatus(_Status):

    chain_separator_regex = r'-{25}\s'

    def __init__(self, archive_dir_path, primary_chain):
        self.archive_dir_path = archive_dir_path
        self.primary_chain = primary_chain

    @property
    def last_full_backup_time(self):
        return self.primary_chain.first_backup_time if self.primary_chain else None

    @property
    def last_incremental_backup_time(self):
        return self.primary_chain.last_incremental_backup_time if self.primary_chain else None

    @classmethod
    def _parse(cls, text):
        if 'No backup chains with active signatures found' in text:
            primary_chain = None
        else:
            primary_chain_match = re.search(
                '^Found primary backup chain.*\s{sep}([\w\W]*?)\s{sep}'.format(
                    sep=_CollectionStatus.chain_separator_regex,
                ),
                text,
                re.MULTILINE,
            )
            primary_chain = _ChainStatus._parse(
                text=primary_chain_match.group(1),
            )
        return cls(
            archive_dir_path=re.search(r'Archive dir: (.*)', text).group(1),
            primary_chain=primary_chain,
        )


class _ChainStatus(_Status):

    def __init__(self, sets):
        self.sets = sets

    @property
    def first_backup_time(self):
        return min([s.backup_time for s in self.sets])

    @property
    def last_backup_time(self):
        return max([s.backup_time for s in self.sets])

    @property
    def last_incremental_backup_time(self):
        return self.last_backup_time if len(self.sets) > 1 else None

    @classmethod
    def _parse(cls, text):
        sets = []
        set_lines = re.split(r'Num volumes: *\r?\n', text)[1]
        for set_line in re.split(r'\r?\n', set_lines):
            set_attr = re.match(
                r'\s*(?P<mode>\w+) {2,}(?P<ts>.+?) {2,} (?P<vol>\d+)',
                set_line,
            ).groupdict()
            # duplicity uses time.asctime().
            # time.strptime() without format inverts time.asctime().
            sets.append(_SetStatus(
                backup_time=_parse_duplicity_timestamp(set_attr['ts']),
            ))
        return cls(sets=sets)


class _SetStatus(_Status):

    def __init__(self, backup_time):
        self.backup_time = backup_time
