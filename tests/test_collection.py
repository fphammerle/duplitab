import pytest

import duplitab
import datetime


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


@pytest.mark.parametrize(('url', 'expected_status'), [
    [
        'file://tests/data/collections/empty/multiple-full',
        duplitab._CollectionStatus(
            primary_chain=duplitab._ChainStatus(
                sets=[
                    duplitab._SetStatus(backup_time=datetime.datetime(2016, 10, 27, 19, 57, 47)),
                    duplitab._SetStatus(backup_time=datetime.datetime(2016, 10, 27, 19, 57, 54)),
                ]),
        ),
    ],
])
def test_collection_request_status(url, expected_status):
    c = duplitab.Collection(url=url)
    assert expected_status == c.request_status()
