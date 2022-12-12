# default files

Explains the config of all default files.

All default files can be copied, renamed and edited to fit your needs.

## 1 properties.default.json

This file contains all part/product properties, which are required for this app.

- **Location**: [/pytia_title_block/resources/properties.default.json](../pytia_title_block/resources/properties.default.json)
- **Rename to**: `properties.json`

### 1.1 file content

```json
{
    "partnumber": "partnumber",
    "revision": "revision",
    "definition": "definition",
    "machine": "pytia.machine",
    "material": "pytia.material",
    "base_size": "pytia.base_size",
    "tolerance": "pytia.tolerance",
    "creator_3d": "pytia.creator"
}
```

### 1.2 description

name | type | description
--- | --- | ---
`generic` | `str` | The name of the property, which stores the value of `generic`.

Important note: Properties are distinguished between catia standard properties und user reference properties.

Standard properties have the following names:

- partnumber
- definition
- revision
- nomenclature
- source
- description

User reference properties can have any name, except all from the list above.

## 2 title_block_items.default.json

This file contains all possible component names in a catia drawing document.

- **Location**: [/pytia_title_block/resources/title_block_items.default.json](../pytia_title_block/resources/title_block_items.default.json)
- **Rename to**: `title_block_items.json`

### 2.1 file content

```json
{
    "partnumber": "value.partnumber",
    "revision": "value.revision",
    "definition": "value.definition",
    "machine": "value.machine",
    "material": "value.material",
    "base_size": "value.base_size",
    "tolerance": "value.tolerance",
    "release_date": "value.release_date",
    "document_type": "value.document_type",
    "scale": "value.scale",
    "creator_3d": "value.creator_3d",
    "creator_2d": "value.creator_2d",
    "notes": "value.notes",
    "version": "value.version",
    "path": "value.path"
}
```

### 2.2 description

name | type | description
--- | --- | ---
`generic` | `str` | The name of the property, which stores the value of `generic`.
