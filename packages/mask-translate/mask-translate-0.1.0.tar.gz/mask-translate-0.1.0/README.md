# Mask Translate

MaskTranslate is a CLI app that creates locale for your app that masks all characters with the full-block unicode character. It can be used for givng visual clue of translation progress or take screenshots of website without its text.

## Roadmap

- [ ] Primitive mode
- [ ] Smart mode for Angular
- [ ] Docker image for integration in CI/CD
- [ ] Smart mode auto-detect

## Supported Platform (or Frameworks)

- Angular with i18n

## Installation

Coming soon to pipx or pip

## How to Use

### Primitive Mode

```shell
cat ~/string.file mask-translate > strings-masked.file
```

### Framework Aware


```shell
mask-translate --platform=angular --name=glyph .
```

This tells masktranslate to create a masked version of the translation given that it is angular

Coming soon
```shell
maske-translate .
```

Leaving all details, MaskTranslate will detect the platform/technology and create a stings file using the default name.

## Use Cases

### Integrating Docker Image in CI/CD

TBA

### Screenshot of masked app version
