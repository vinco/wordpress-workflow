# -*- coding: utf-8 -*-


VERSIONS = [
    '0.1',
]


def update(entry):
    version = entry[0]
    idx = VERSIONS.index(version)
    for currv, nextv in zip(VERSIONS, VERSIONS[1:])[idx:]:
        yield globals()[
            'update_%s_to_%s' % (
                currv.replace('.', '_'), nextv.replace('.', '_')
            )
        ]()


def update_0_1_to_1_0():
    '''
    Agrega la tabla coupons (descuentos)
    '''
    return  {
    }


def create_configuration():
    return '''
        DROP TABLE IF EXISTS configurationstore;
        CREATE TABLE "configurationstore" (
            id int(11) NOT NULL AUTO_INCREMENT,
            clave varchar(50) NOT NULL,
            valor varchar(50) NOT NULL,
            PRIMARY KEY(id),
            UNIQUE KEY(clave)
        ) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
        INSERT INTO configurationstore values(null, 'version', '0.1');
    '''
