import unittest


class TestReadMe(unittest.TestCase):
    """Test README.md advanced usage example."""

    def test_01_readme(self):
        """Test readme."""

        # START README.md

        try:
            import fgr

            class Flea(fgr.Object):
                """A nuisance."""

                name: fgr.Field[str] = 'FLEA'


            class Pet(fgr.Object):
                """A pet."""

                id_: fgr.Field[str]
                _alternate_id: fgr.Field[int]

                name: fgr.Field[str]
                type_: fgr.Field[str] = {
                    'default': 'dog',
                    'enum': ['cat', 'dog'],
                    'nullable': False,
                    'required': True,
                    }

                in_: fgr.Field[str]
                is_tail_wagging: fgr.Field[bool] = fgr.Field(
                    default=True,
                    enum=[True, False],
                    nullable=False,
                    required=True,
                    )

                fleas: fgr.Field[list[Flea]] = [
                    Flea(name='flea1'),
                    Flea(name='flea2')
                    ]


            # Automatic case handling.
            request_body = {
                'id': 'abc123',
                'alternateId': 123,
                'name': 'Bob',
                'type': 'dog',
                'in': 'timeout',
                'isTailWagging': False
                }
            pet = Pet(request_body)

            assert pet.is_snake_case == Pet.is_snake_case is True
            assert pet.isCamelCase == Pet.isCamelCase is False
            assert pet['alternate_id'] == pet._alternate_id == request_body['alternateId']
            assert dict(pet) == {k: v for k, v in pet.items()} == pet.to_dict()

            # Automatic, mutation-safe "default factory".
            dog = Pet(id='abc321', alternate_id=321, name='Fido')
            assert pet.fleas[0] is not dog.fleas[0]

            # Automatic memory optimization.
            assert Flea().__sizeof__() == (len(Flea.__slots__) * 8) + 16 == 24

            class Flet(Flea, Pet):
                ...

            class Pea(Pet, Flea):
                ...

            assert Flet().__sizeof__() == (len(Flet.__base__.__slots__) * 8) + 16 == 72
            assert Pea().__sizeof__() == (len(Pea.__base__.__slots__) * 8) + 16 == 72
            assert Flet().name == 'FLEA' != Pea().name

            # Intuitive, database agnostic query generation.
            assert isinstance(Pet.is_tail_wagging, fgr.Field)
            assert isinstance(Pet.type_, fgr.Field)

            assert dog.type_ == Pet.type_.default == 'dog'

            query = (
                (
                    (Pet.type_ == 'dog')
                    & (Pet.name == 'Fido')
                    )
                | Pet.name % ('fido', 0.75)
                )
            query += 'name'
            assert dict(query) == {
                'limit': None,
                'or': [
                    {
                        'and': [
                            {
                                'eq': 'dog',
                                'field': 'type',
                                'limit': None,
                                'sorting': []
                                },
                            {
                                'eq': 'Fido',
                                'field': 'name',
                                'limit': None,
                                'sorting': []
                                }
                            ],
                        'limit': None,
                        'sorting': []
                        },
                    {
                        'field': 'name',
                        'like': 'fido',
                        'limit': None,
                        'sorting': [],
                        'threshold': 0.75
                        }
                    ],
                'sorting': [
                    {
                        'direction': 'asc',
                        'field': 'name'
                        }
                    ]
                }

            # END README.md

        except AssertionError:
            self.assertTrue(False)
        else:
            self.assertTrue(True)
