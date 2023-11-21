# Changelog

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)

- `Added` - for new features.
- `Changed` - for changes in existing functionality.
- `Deprecated` - for soon-to-be removed features.
- `Removed` - for now removed features.
- `Fixed` - for any bug fixes.
- `Security` - in case of vulnerabilities.

## [1.3.0] - 2023-10-23

### Added

- [TACIAD-5736](https://jira-eng-sjc1.cisco.com/jira/browse/TACIAD-5736) - Added Source URL field to capture the activity page URL.

### Fixed

- [TACIAD-5737](https://jira-eng-sjc1.cisco.com/jira/browse/TACIAD-5737) - Updated backend container dependencies and fixed the issue with displaying unit test count on SonarQube report.

## [1.2.1] - 2023-10-13

### Fixed

- [TACIAD-5698](https://jira-eng-sjc1.cisco.com/jira/browse/TACIAD-5698) - Fixed the SonarQube reported code smells as part of Static Code Analysis.

## [1.2.0] - 2023-10-05

### Changed

- [TACIAD-5320](https://jira-eng-sjc1.cisco.com/jira/browse/TACIAD-5320) - Modified POST API to validate user using `orgstats API` and updated GET API response to return SR value as `-777777777` if it is blank / none.
- [TACIAD-5568](https://jira-eng-sjc1.cisco.com/jira/browse/TACIAD-5568) - Migrated to MongoDB Atlas for data storage and hence removed existing MongoDB Container deployment configuration.

## [1.1.0] - 2023-03-08

### Added

- [TACIAD-3409](https://jira-eng-sjc1.cisco.com/jira/browse/TACIAD-3409) - Added static auth token for GET API to fetch Activity records.
- [TACIAD-3413](https://jira-eng-sjc1.cisco.com/jira/browse/TACIAD-3413) - Created an Activity PUT API to update end time.

### Changed

- [TACIAD-3410](https://jira-eng-sjc1.cisco.com/jira/browse/TACIAD-3410) - Allowed all cisco.com subdomains for ACTS Activity API.
- [TACIAD-3412](https://jira-eng-sjc1.cisco.com/jira/browse/TACIAD-3412) - Updated the Activity POST API to calculate start time from duration and return the record Id.

## [1.0.0] - 2023-02-07

### Added

- This project

[1.3.0]: https://gitlab-sjc.cisco.com/cxInnovations/iad/acts/acts-activity/-/compare/1.2.1...1.3.0
[1.2.1]: https://gitlab-sjc.cisco.com/cxInnovations/iad/acts/acts-activity/-/compare/1.2.0...1.2.1
[1.2.0]: https://gitlab-sjc.cisco.com/cxInnovations/iad/acts/acts-activity/-/compare/1.1.0...1.2.0
[1.1.0]: https://gitlab-sjc.cisco.com/cxInnovations/iad/acts/acts-activity/-/compare/1.0.0...1.1.0
[1.0.0]: https://gitlab-sjc.cisco.com/cxInnovations/iad/acts/acts-activity/-/compare/1.0.0...1.0.0
