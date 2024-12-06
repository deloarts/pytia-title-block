# usage

> ✏️ This covers the usage of the app, which depends on the configuration of the `settings.json` config file. If you use different names for properties or disable some of the functionality, the apps layout may be different from the one in this guide.

- [usage](#usage)
  - [1 launcher](#1-launcher)
  - [2 app](#2-app)

## 1 launcher

If your setup is done (see [installation](./INSTALLATION.md)), open the app from within CATIA. If this is the first time, you'll see the launcher will install all necessary dependencies:

![Installer](/assets/images/installer.png)

After the installation you can run the app.

## 2 app

The usage itself is pretty straight forward, as long as all config files are setup properly.

![App](/assets/images/app.png)

The app retrieves all information from the documents properties and writes it to the title block. The user has the option to alter those properties via the app.

If the user runs the app on an existing title block, all data will be fetched from the title block, not from the linked document's properties. If a datum doesn't match (a title block item has a different value than the corresponding property) the corresponding widget will render the text red.

The usage itself is pretty straight forward, as long as all config files are setup properly.

In the assets folder is a [catia drawing file](/assets/title_block_templates/A4_ISO_H_EN.CATDrawing), which works with the app straight away.

![Example](/assets/images/example.png)
