import pytest

import os
import duplitab
import datetime

project_root_path = os.path.realpath(os.path.join(__file__, '..', '..'))
test_data_dir_path = os.path.join(project_root_path, 'tests', 'data')
test_collections_dir_path = os.path.join(test_data_dir_path, 'collections')


@pytest.mark.parametrize(('init_kwargs', 'expected_attr'), [
    [
        {
            'url': 'file://media/backup/a',
        },
        {
            'url': 'file://media/backup/a',
        },
    ],
    [
        {
            'url': 'sftp://user@server//media/backup/阿',
        },
        {
            'url': 'sftp://user@server//media/backup/阿',
        },
    ],
])
def test_collection_init(init_kwargs, expected_attr):
    c = duplitab.Collection(**init_kwargs)
    for name, value in expected_attr.items():
        assert getattr(c, name) == value


@pytest.mark.parametrize(('init_kwargs', 'ex_class'), [
    [
        {
        },
        TypeError,
    ],
])
def test_collection_init_fail(init_kwargs, ex_class):
    with pytest.raises(ex_class):
        duplitab.Collection(**init_kwargs)


@pytest.mark.parametrize(('url', 'expected_status_attr'), [
    [
        'file://{}'.format(os.path.join(test_collections_dir_path, 'empty', 'only-full')),
        {
            'primary_chain': duplitab._ChainStatus(
                sets=[
                    duplitab._SetStatus(backup_time=datetime.datetime(2016, 10, 27, 19, 57, 33)),
                ]),
        },
    ],
    [
        'file://{}'.format(os.path.join(test_collections_dir_path, 'empty', 'single-full')),
        {
            'primary_chain': duplitab._ChainStatus(
                sets=[
                    duplitab._SetStatus(backup_time=datetime.datetime(2016, 10, 27, 19, 57, 33)),
                    duplitab._SetStatus(backup_time=datetime.datetime(2016, 10, 27, 19, 57, 35)),
                    duplitab._SetStatus(backup_time=datetime.datetime(2016, 10, 27, 19, 57, 39)),
                ]),
        },
    ],
    [
        'file://{}'.format(os.path.join(test_collections_dir_path, 'empty', 'multiple-full')),
        {
            'primary_chain': duplitab._ChainStatus(
                sets=[
                    duplitab._SetStatus(backup_time=datetime.datetime(2016, 10, 27, 19, 57, 47)),
                    duplitab._SetStatus(backup_time=datetime.datetime(2016, 10, 27, 19, 57, 54)),
                ]),
        },
    ],
    [
        'file://{}'.format(os.path.join(test_collections_dir_path, 'none')),
        {
            'primary_chain': None,
        },
    ],
])
def test_collection_request_status(url, expected_status_attr):
    c = duplitab.Collection(url=url)
    s = c.request_status()
    assert not s.archive_dir_path is None
    for name, value in expected_status_attr.items():
        assert value == getattr(s, name)


@pytest.mark.parametrize(('chain_status', 'expected_time'), [
    [
        duplitab._ChainStatus(
            sets=[
                duplitab._SetStatus(backup_time=datetime.datetime(2016, 10, 27, 19, 57, 33)),
            ]),
        datetime.datetime(2016, 10, 27, 19, 57, 33),
    ],
    [
        duplitab._ChainStatus(
            sets=[
                duplitab._SetStatus(backup_time=datetime.datetime(2016, 10, 27, 19, 57, 33)),
                duplitab._SetStatus(backup_time=datetime.datetime(2016, 10, 27, 19, 57, 35)),
                duplitab._SetStatus(backup_time=datetime.datetime(2016, 10, 27, 19, 57, 39)),
            ]),
        datetime.datetime(2016, 10, 27, 19, 57, 39),
    ],
])
def test_chain_status_get_last_backup_time(chain_status, expected_time):
    assert expected_time == chain_status.last_backup_time


@pytest.mark.parametrize(('chain_status', 'expected_time'), [
    [
        duplitab._ChainStatus(
            sets=[
                duplitab._SetStatus(backup_time=datetime.datetime(2016, 10, 27, 19, 57, 33)),
            ]),
        datetime.datetime(2016, 10, 27, 19, 57, 33),
    ],
    [
        duplitab._ChainStatus(
            sets=[
                duplitab._SetStatus(backup_time=datetime.datetime(2016, 10, 27, 19, 57, 33)),
                duplitab._SetStatus(backup_time=datetime.datetime(2016, 10, 27, 19, 57, 35)),
                duplitab._SetStatus(backup_time=datetime.datetime(2016, 10, 27, 19, 57, 39)),
            ]),
        datetime.datetime(2016, 10, 27, 19, 57, 33),
    ],
])
def test_chain_status_get_first_backup_time(chain_status, expected_time):
    assert expected_time == chain_status.first_backup_time


@pytest.mark.parametrize(('collection_status', 'expected_time'), [
    [
        duplitab._CollectionStatus(
            archive_dir_path='/tmp/none',
            primary_chain=duplitab._ChainStatus(
                sets=[
                    duplitab._SetStatus(backup_time=datetime.datetime(2016, 10, 27, 19, 57, 33)),
                ]),
        ),
        datetime.datetime(2016, 10, 27, 19, 57, 33),
    ],
    [
        duplitab._CollectionStatus(
            archive_dir_path='/tmp/none',
            primary_chain=duplitab._ChainStatus(
                sets=[
                    duplitab._SetStatus(backup_time=datetime.datetime(2016, 10, 27, 19, 57, 33)),
                    duplitab._SetStatus(backup_time=datetime.datetime(2016, 10, 27, 19, 57, 35)),
                    duplitab._SetStatus(backup_time=datetime.datetime(2016, 10, 27, 19, 57, 39)),
                ]),
        ),
        datetime.datetime(2016, 10, 27, 19, 57, 39),
    ],
    [
        duplitab._CollectionStatus(
            archive_dir_path='/tmp/none',
            primary_chain=None,
        ),
        None,
    ],
])
def test_collection_status_get_last_incremental_backup_time(
        collection_status, expected_time):
    assert expected_time == collection_status.last_incremental_backup_time

@pytest.mark.parametrize(('collection_status', 'expected_time'), [
    [
        duplitab._CollectionStatus(
            archive_dir_path='/tmp/none',
            primary_chain=duplitab._ChainStatus(
                sets=[
                    duplitab._SetStatus(backup_time=datetime.datetime(2016, 10, 27, 19, 57, 33)),
                ]),
        ),
        datetime.datetime(2016, 10, 27, 19, 57, 33),
    ],
    [
        duplitab._CollectionStatus(
            archive_dir_path='/tmp/none',
            primary_chain=duplitab._ChainStatus(
                sets=[
                    duplitab._SetStatus(backup_time=datetime.datetime(2016, 10, 27, 19, 57, 33)),
                    duplitab._SetStatus(backup_time=datetime.datetime(2016, 10, 27, 19, 57, 35)),
                    duplitab._SetStatus(backup_time=datetime.datetime(2016, 10, 27, 19, 57, 39)),
                ]),
        ),
        datetime.datetime(2016, 10, 27, 19, 57, 33),
    ],
    [
        duplitab._CollectionStatus(
            archive_dir_path='/tmp/none',
            primary_chain=None,
        ),
        None,
    ],
])
def test_collection_status_get_incremental_backup_time(
        collection_status, expected_time):
    assert expected_time == collection_status.last_full_backup_time
