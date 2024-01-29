# sample files

Explains the config of all sample files.

All sample files must be copied, renamed and edited to fit your needs.

## 1 settings.sample.json

This file contains the basic settings for the app.

- **Location**: [/pytia_title_block/resources/settings.sample.json](../pytia_title_block/resources/settings.sample.json)
- **Rename to**: `settings.json`

### 1.1 file content

```json
{
    "title": "PYTIA Title Block Editor",
    "debug": false,
    "restrictions": {
        "allow_all_users": true,
        "allow_all_editors": true,
        "allow_unsaved": true,
        "allow_outside_workspace": true,
        "allow_locked_view": false
    },
    "doc_types": [
        "Production",
        "Test",
        "Assembly"
    ],
    "tolerances": [
        "ISO 2768 1-m 2-K",
        "ISO 2768 1-f 2-K",
        "ISO 2768 1-c 2-K",
        "ISO 2768 1-v 2-K"
    ],
    "tables": {
        "tolerances": {
            "header_base": "Base",
            "header_min": "Minimum",
            "header_max": "Maximum",
            "positions": [
                {
                    "size": "A4",
                    "x": 107,
                    "y": 10
                },
                {
                    "size": "A3",
                    "x": 230,
                    "y": 10
                },
                {
                    "size": "A2",
                    "x": 404,
                    "y": 10
                },
                {
                    "size": "A1",
                    "x": 651,
                    "y": 10
                },
                {
                    "size": "A0",
                    "x": 999,
                    "y": 10
                }
            ]
        }
    },
    "paths": {
        "catia": "C:\\CATIA\\V5-6R2017\\B27",
        "release": "C:\\pytia\\release"
    },
    "files": {
        "app": "pytia_title_block.pyz",
        "launcher": "pytia_title_block.catvbs",
        "workspace": "workspace.yml"
    },
    "urls": {
        "help": null
    },
    "mails": {
        "admin": "admin@company.com"
    }
}
```

### 1.2 description

name | type | description
--- | --- | ---
title | `str` | The apps title. This will be visible in the title bar of the window.
debug | `bool` | The flag to declare the debug-state of the app. The app cannot be built if this value is true.
restrictions.allow_all_users | `bool` | If set to `true` any user can make changes to the documents properties. If set to `false` only those users from the **users.json** file can modify the properties.
restrictions.allow_all_editors | `bool` | If set to `true` any user can make changes to the documents properties. If set to `false` only those users which are declared in the **workspace** file can modify the properties. If no workspace file is found, or no **editors** list-item is inside the workspace file, then this is omitted, and everyone can make changes.
restrictions.allow_unsaved | `bool` | If set to `false` an unsaved document (a document which doesn't have a path yet) cannot be modified.
restrictions.allow_outside_workspace | `bool` | If set to `false` a **workspace** file must be provided somewhere in the folder structure where the document is saved. This also means, that an unsaved document (a document which doesn't have a path yet) cannot be modified.
restrictions.allow_locked_view | `bool` | If set to `false` the user cannot make any changes if the first view is locked. This helps to prevent changes after the document has been released.
doc_types | `List[str]` | A list of available document types.
tolerances | `List[str]` | A list of available tolerances.
tables.tolerances.header_base | `str` | The table header name for the tolerance base value.
tables.tolerances.header_min | `str` | The table header name for the tolerance minimum value.
tables.tolerances.header_max | `str` | The table header name for the tolerance maximum value.
tables.tolerances.positions | `List[Object]` | The table position depending on the paper size. Anchor is bottom right.
paths.catia | `str` | The absolute path to the CATIA executables. Environment variables will be expanded to their respective values. E.g: `%ONEDRIVE%\\CATIA\\Apps` will be resolved to `C:\\Users\\...\\OneDrive\\CATIA\\Apps`.
paths.release | `str` | The folder where the launcher and the app are released into. Environment variables will be expanded to their respective values. E.g: `%ONEDRIVE%\\CATIA\\Apps` will be resolved to `C:\\Users\\...\\OneDrive\\CATIA\\Apps`.
files.app | `str` | The name of the released python app file.
files.launcher | `str` | The name of the release catvbs launcher file.
files.material | `str` | The filename of CATMaterial file.
files.workspace | `str` | The name of the workspace file.
urls.help | `str` or `null` | The help page for the app. If set to null the user will receive a message, that no help page is provided.
mails.admin | `str` | The mail address of the sys admin. Required for error mails.

## 2 users.sample.json

This file contains a list of users known to the system.

- **Location**: [/pytia_title_block/resources/users.sample.json](../pytia_title_block/resources/users.sample.json)
- **Rename to**: `users.json`

### 2.1 file content

```json
[
    {
        "logon": "admin",
        "id": "001",
        "name": "Administrator",
        "mail": "admin@company.com"
    },
    ...
]
```

### 2.2 description

name | type | description
--- | --- | ---
logon | `str` | The windows logon name of the user in lowercase.
id | `str` | The ID of the user. Can be used for the employee ID.
name | `str` | The name of the user.
mail | `str` | The users mail address.
