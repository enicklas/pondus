# Handling Translations for Pondus

## Transifex

Translations can be created or updated via
[Transifex](https://www.transifex.net/projects/p/pondus/).

## The manual way

### Creating a new translation

Run `msginit` in `po/` and follow the instructions.

Alternatively, you can also copy `pondus.pot` to `LL.po` (where LL is
your language code) and edit the header manually.

Translate the strings and send the resulting `LL.po` to
&lt;<pondus-dev@lists.berlios.de>&gt;

### Updating a translation

Shortly before new releases, a notification will be sent to the mailing
list asking for an update of the translations. Then, you can download
the `LL.po` file from the hg repository, translate new strings, correct
changed strings and send the resulting `LL.po` to
&lt;<pondus-dev@lists.berlios.de>&gt;
