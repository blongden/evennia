# Generated by Django 3.2.9 on 2022-01-07 17:01

from django.db import migrations

PATH_REMAP_PREFIX = {
    "ingame_python": "evennia.contrib.base_systems",
    "building_menu": "evennia.contrib.base_systems",
    "color_markups": "evennia.contrib.base_systems",
    "custom_gametime": "evennia.contrib.base_systems",
    "email_login": "evennia.contrib.base_systems",
    "ingame_python": "evennia.contrib.base_systems",
    "menu_login": "evennia.contrib.base_systems",
    "mux_cmms_cmds": "evennia.contrib.base_systems",
    "unixommand": "evennia.contrib.base_systems",
    "evscaperoom": "evennia.contrib.full_systems",
    "barter": "evennia.contrib.game_systems",
    "clothing": "evennia.contrib.game_systems",
    "cooldowns": "evennia.contrib.game_systems",
    "crafting": "evennia.contrib.game_systems",
    "gendersub": "evennia.contrib.game_systems",
    "mail": "evennia.contrib.game_systems",
    "multidescer": "evennia.contrib.game_systems",
    "puzzles": "evennia.contrib.game_systems",
    "turnbattle": "evennia.contrib.game_systems",
    "extended_room": "evennia.contrib.grid",
    "mapbuilder": "evennia.contrib.grid",
    "simpledoor": "evennia.contrib.grid",
    "slow_exit": "evennia.contrib.grid",
    "wilderness": "evennia.contrib.grid",
    "xyzgrid": "evennia.contrib.grid",
    "dice": "evennia.contrib.rpg",
    "health_bar": "evennia.contrib.rpg",
    "rpsystem": "evennia.contrib.rpg.rpsystem",
    "rplanguage": "evennia.contrib.rpg.rpsystem",
    "traits": "evennia.contrib.rpg",
    "batchprocessor": "evennia.contrib.tutorials",
    "bodyfunctions": "evennia.contrib.tutorials",
    "mirror": "evennia.contrib.tutorials",
    "red_button": "evennia.contrib.tutorials",
    "tutorial_world": "evennia.contrib.tutorials",
    "auditing": "evennia.contrib.utils",
    "fieldfill": "evennia.contrib.utils",
    "random_string_generator": "evennia.contrib.utils",
    "tree_select": "evennia.contrib.utils"
}


def convert_contrib_typeclass_paths(apps, schema_editor):
    AccountDB = apps.get_model("accounts", "AccountDB")

    for obj in AccountDB.objects.filter(db_typeclass_path__startswith="evennia.contrib."):
        try:
            package_path = obj.db_typeclass_path.split(".")[2:]
            package_name = package_path[0]
            if package_path[0] == 'security':
                # renamed package and changed path
                package_name = 'auditing'
                package_path.pop(0)  # no longer security/auditing
            if package_path[-1] == ".Clothing":
                # renamed Clothing class to ContribClothing
                package_path[-1] = "ContribClothing"
            package_path = '.'.join(package_path)

        except IndexError:
            print(f"obj.db_typeclass_path={obj.db_typeclass_path} could not be parsed "
                  "for converting to the new contrib location.")
            continue
        if package_name in PATH_REMAP_PREFIX:
            obj.db_typeclass_path = f"{PATH_REMAP_PREFIX[package_name]}.{package_path}"
            obj.save(update_fields=['db_typeclass_path'])

    for obj in AccountDB.objects.filter(db_cmdset_storage__startswith="evennia.contrib."):
        try:
            package_path = obj.db_cmdset_storage.split(".")[2:]
            package_name = package_path[0]
            package_path = '.'.join(package_path)
        except IndexError:
            print(f"obj.db_cmdset_storage={obj.db_cmdset_storage} could not be parsed "
                  "for converting to the new contrib location.")
            continue
        if package_name in PATH_REMAP_PREFIX:
            obj.db_cmdset_storage = f"{PATH_REMAP_PREFIX[package_name]}.{package_path}"
            obj.save(update_fields=['db_cmdset_storage'])


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_auto_20210520_2137'),
    ]

    operations = [
        migrations.RunPython(convert_contrib_typeclass_paths, migrations.RunPython.noop)
    ]
