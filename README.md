# D3 CI Actions

Zentrale Sammlung wiederverwendbarer GitHub Composite Actions für CI-Pipelines.

Ziel dieses Repositories ist es, CI-Logik zu standardisieren, Copy-Paste zu vermeiden und Workflows in Projekt-Repositories schlank zu halten.

## Grundprinzipien

Dieses Repository enthält nur Actions, keine Projekt-Pipelines. Die Actions sind bewusst klein, fokussiert und generisch konzipiert. Infrastruktur, 
Secrets und Matrix-Logik sollen bitte im verwendenden Projekt definiert werden. Jeder Ordner enthält genau eine Composite Action.

## Versionierung

Dieses Repository verwendet semantische Versionierung über Git-Tags.

Empfohlene Nutzung in Projekten:

```
uses: d3datadevelopment/ci-actions/<action-name>@v1
```

`v1` zeigt immer auf die aktuelle stabile Version der Major-Reihe. In `rel_X.x` befindet sich die aktuellste Pre-Release Version.

## Enthaltene Actions
### oxid-test-runner
  Führt OXID Plugin Tests in einer reproduzierbaren Umgebung aus. Verfügbar für Plugins ab OXID 7.0.

#### Tasks
  - PHP einrichten
  - optional SourceGuardian aktivieren
  - optional PHP Syntax-Check
  - OXID Shop installieren & konfigurieren
  - Theme aktivieren (falls unterstützt)
  - Plugin installieren & aktivieren
  - PHPUnit installieren
  - Unit- und/oder Integration-Tests ausführen

#### Inputs

| Name                  | Typ    | Pflicht | Beschreibung                          | Beispiel           |
|-----------------------|--------|---------|---------------------------------------|--------------------|
| php_version           | string | ja      | PHP-Version                           | "8.0"              |
| oxid_ref              | string | ja      | OXID Version                          | "dev-b-7.4-ce"     |
| phpunit_version       | string | ja      | PHPUnit Version                       | "^9.0"             |
| sourceguardian        | bool   | nein    | SourceGuardian aktivieren             | "true"             |
| composer_package_name | string | ja      | Composer Package Name                 | "d3/mypackage"     |
| oxid_module_id        | string | nein    | OXID Module ID zur Aktivierung        | "d3mymodule"       |
| test_suites           | string | nein    | kommagetrennte PHPUnit Suites         | "unit,integration" |
| syntax_check_paths    | string | nein    | kommagetrennte Pfade für Syntax-Check | "src,tests"        |

#### Erwartete ENV-Variablen

Diese müssen vom Workflow gesetzt werden:

- DB_HOST
- DB_NAME
- DB_USER
- DB_PASS
- DB_PORT (optional, Default 3306)

#### Beispiel

```
- name: Run OXID plugin tests
  uses: d3datadevelopment/ci-actions/oxid-plugin-test@v1
  with:
    php_version: "8.2"
    oxid_ref: "dev-b-7.1-ce"
    phpunit_version: "^10"
    composer_package_name: "d3/mailconfigchecker"
    oxid_module_id: "d3mailconfigchecker"
    test_suites: "unit,integration"
    syntax_check_paths: "src,tests"
```
### composer-package-test-runner

Führt Tests für reine Composer-Pakete aus (ohne OXID).

#### Tasks
- PHP einrichten
- Composer Dependencies installieren
- optional PHP Syntax-Check
- PHPUnit Tests ausführen

#### Inputs
| Name               | Typ    | Pflicht | Beschreibung                          | Beispiel           |
|--------------------|--------|---------|---------------------------------------|--------------------|
| php_version        | string | ja      | PHP-Version                           | "8.4"              |
| test_suites        | string | nein    | PHPUnit Testsuites (kommagetrennt)    | "unit,integration" |
| syntax_check_paths | string | nein    | kommagetrennte Pfade für Syntax-Check | "src,tests"        |

#### Beispiel

```
- name: Run package tests
  uses: d3datadevelopment/ci-actions/composer-package-test@v1
  with:
    php_version: "8.2"
    syntax_check_paths: "src,Tests"
    test_suites: "unit,integration"
```

### commit-status-reporter

Sendet einen CI-Status an einen beliebigen HTTP-Endpunkt.

#### Inputs
| Name            | Typ    | Pflicht | Beschreibung                        | Beispiel                             |
|-----------------|--------|---------|-------------------------------------|--------------------------------------|
| status_endpoint | string | ja      | Vollständige API-URL                | "https://mydomain.example/statuses/" |
| auth_token      | string | ja      | Auth-Token (via Repository Secrets) | "abcdef"                             |
| state           | string | ja      | Ausführungsstatus                   | "success", "failure", ...            |
| context         | string | nein    | Status-Kontext                      | "ci/github"                          |
| description     | string | nein    | Beschreibung                        | "CI passed"                          |
| target_url      | string | nein    | Workflow URL mit Build-Details      |                                      |

#### Beispiel

```
- name: Report CI status
  uses: d3datadevelopment/ci-actions/status-reporter@v1
  with:
    status_endpoint: https://mydomain.example/statuses/${{ github.sha }}
    auth_token: ${{ secrets.STATUS_TOKEN }}
    state: success
    description: "CI passed"
    target_url: ${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}
```

### AI Changelog Generator

erstellt beim Änderungen innerhalb eines Release Branches auf Basis der Commit Messages einen technisch orientiertes Changelog Abschnitt für
alle Änderungen seit dem letzten Tag.

#### Inputs
| Name            | Typ    | Pflicht | Beschreibung                               | Beispiel                            |
|-----------------|--------|---------|--------------------------------------------|-------------------------------------|
| openai_api_key  | string | ja      | API-Key für OpenAI (ChatGpt)               | "abcdef"                            |
| repo_url        | string | ja      | Repository URL                             | "https://git.mydomain.example/..."  |
| push_token      | string | ja      | Token mit Push-Berechtigung im Remote Repo | "abcdef"                            |

#### Beispiel

```
name: Release Changelog

on:
  push:
    branches:
      - 'rel_*'

  workflow-dispatch:

jobs:
  changelog:
    runs-on: ubuntu-latest


    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0


      - name: Generate AI changelog
        uses: ./.github/actions/ai-changelog@dev-1.x-autochangelog
        with:
          openai_api_key: ${{ secrets.OPENAI_API_KEY }}
          repo_url: https://git.mydomain.com/OWNER/REPO
          push_token: ${{ secrets.GITEA_PUSH_TOKEN }}
```

## Beispiele

Schaue in [CI Tests](https://github.com/d3datadevelopment/CI-Tests) für Integrationsbeispiele.

## Selbsttests

Dieses Repository enthält Workflows, die die Aktionen selbst testen.
Die Tests werden anhand externer Test-Repositorys durchgeführt, die echten, ausführbaren Code enthalten.

Diese Workflows werden automatisch ausgelöst, wenn Änderungen an den entsprechenden Aktionsverzeichnissen vorgenommen werden.