# sitecheck# sitecheck

A pre-deployment checklist CLI for websites, starting with generic website checks and WordPress support.

## Status

Early development.  
The project is currently being built and the first goal is to get the CLI foundation working before adding real checks.

## Why this project exists

Deployments for websites are often inconsistent, especially on smaller projects.  
It is easy to forget things like:

- debug mode still being enabled
- missing environment setup
- missing backup steps
- risky files left in place
- WordPress-specific production issues

The goal of `sitecheck` is to help developers catch common deployment problems before shipping.

## Initial scope

Version 1 will focus on:

- generic website/project checks
- WordPress-specific checks
- clear pass / warn / fail output
- simple local CLI usage

Example future usage:

```bash
sitecheck scan .
sitecheck scan . --profile wordpress