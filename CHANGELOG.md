# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- Support for [ECDA signing](https://encryptionconsulting.com/education-center/what-is-ecdsa/) 
- Payment page and integration with payment processor.
- Interface API for controlling a door.
- Proper logging system for events.
- Proper notification system for unusual activity.
- Added http test suite with http prompt
- basic request/response authenticaion service server
- basic logger for authentication events
- interface for communicating with door controllers (ZKTecco)
- Repeatable installation script
- testing Debian 11 VM

### Changed
- Rearranged folder structure.

## [0.0.1] - 2021-12-30
### Added
- User login and registration pages
- Basic home page
- APIs for logging in and creating a user
- API for creating user-specific QR code
