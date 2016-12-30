include:
  - heroku.apt

apt-update:
  cmd:
    - run
    - name: apt-get update

heroku:
  pkg:
    - latest
    - names:
      - heroku-toolbelt
    - require:
      - cmd: apt-update
