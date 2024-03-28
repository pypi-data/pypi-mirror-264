from ophis.database import Repository, QueryParams
from pytest import fail


def test_crud(thing_data):
    # Nothing here
    assert thing_data.get('012345678912', item_id="test") is None
    # Create
    things = []
    for index in range(0, 9):
        thing = thing_data.create('012345678912', item={
            'thingName': f'MyThing{index}',
        })
        assert thing['thingName'] == f'MyThing{index}'
        things.append(thing)
    try:
        thing_data.create('012345678912', item={
            'thingName': 'MyThing0'
        })
        fail('Should not have gotten here')
    except Exception as e:
        assert str(e) == 'The Things item already exists.'
    # Read
    assert things[0] == thing_data.get('012345678912', item_id='MyThing0')
    # List
    assert things == thing_data.items('012345678912').items
    # Pagination
    resp = thing_data.items('012345678912', params=QueryParams(limit=3))
    assert things[0:3] == resp.items
    assert resp.next_token is not None
    # Next Page
    resp = thing_data.items('012345678912', params=QueryParams(limit=3, next_token=resp.next_token))
    assert things[3:6] == resp.items
    assert resp.next_token is not None
    # Delete
    thing_data.delete('012345678912', item_id="MyThing0")
    assert thing_data.get('012345678912', item_id='MyThing0') is None
    try:
        thing_data.update('012345678912', item={'thingName': 'MyThing0'})
        fail('Should not have gotten here')
    except Exception as e:
        assert str(e) == "The Things item does not exist."
    # Batch Read
    batched = Repository.batch_read('012345678912', reads=[
        {
            'id': 'Nothing',
        },
        {
            'repository': thing_data,
            'id': 'MyThing1',
        }
    ])
    assert things[1:2] == batched
    # Batch Write
    Repository.batch_write('012345678912', updates=[
        {
            'id': 'Nothing',
        },
        {
            'repository': thing_data,
            'item': {
                'thingName': 'MyBatchedThing0'
            }
        },
        {
            'repository': thing_data,
            'item': {
                'thingName': 'MyThing1'
            },
            'delete': True
        }
    ])
    assert thing_data.get('012345678912', item_id='MyBatchedThing0') is not None
    assert thing_data.get('012345678912', item_id='MyThing1') is None
