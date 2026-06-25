# automated-transcription-service

Social science researchers using qualitative methods, especially in-depth interviews and focus groups, typically need audio recordings transcribed into accurate text for analysis. Currently, many researchers use other automated transcription services, such as Temi, Trint, or Otter.ai, which are well-known to social science researchers and provide easy-to-use web interfaces for uploading multiple audio files, and then downloading multiple transcripts. These services are also more accessible to graduate students, who do not have internal departmental account numbers for billing and typically pay out-of-pocket for these external services. However, these services come with important data security concerns. Most of these services do not provide the kinds of security documentation required for data steward approval, and many will not have signed a Business Associate Agreement with the university, meaning that they are not approved for use with HIPAA-protected data.

We believe that cloud machine learning APIs provides a powerful alternative to researchers. Thus far, social scientists have not made full use of this option, in part, we believe, because using these services efficiently requires additional technical skills that many social scientists do not have, and/or do not have time to learn. Other social scientists, especially graduate students, have used these services, but do not have access to the same cloud environment as faculty—meaning that their data, when stored in a free or student account, do not receive the same security protections. 

Thus, we seek to provide a new service to researchers that will make audio transcription convenient, efficient, and accessible to them, even without technical skills. For researchers, this will provide an affordable and secure option for quickly producing automated transcripts of research-related recordings.

This project has folders:
* aws: To build a pipeline with terraform to accept audio files in an S3 input bucket and convert those to docx with the help of a Python script. Output files are placed in another S3 output bucket
* google: Python script to convert json to text or docx only

## Versioning & Releases

This is a fork of [indiana-university/automated-transcription-service](https://github.com/indiana-university/automated-transcription-service) with additional customizations for use as a Git submodule in Terraform deployments.

### Version scheme

Releases follow the format `<upstream-version>-rci.<increment>`:

- `2.3.1-rci.1` = based on upstream v2.3.1, first RCI release
- `2.3.1-rci.2` = based on upstream v2.3.1, second RCI release
- `2.4.0-rci.1` = synced to upstream v2.4.0, first RCI release on that base

### Pinning as a submodule

Reference a specific release tag in your Terraform module:

```hcl
source = "git::https://github.com/ORC-RIS/automated-transcription-service.git?ref=v2.3.1-rci.1"
```

### Release process

1. Feature/bugfix branches are created from `develop` and merged back via squash merge.
2. A release candidate branch (`rc-X.X.X-rci.N`) is created from `develop`.
3. The RC is merged into `main` with a merge commit.
4. A GitHub release is tagged on `main` (e.g., `v2.3.1-rci.1`).

### Syncing with upstream

When ready to incorporate upstream changes:

```bash
git fetch upstream
git merge upstream/main
```

This updates `main` to the latest upstream release, after which new RCI changes are versioned against the new base (e.g., `v2.4.0-rci.1`).