# CHANGELOG



## v0.1.6 (2024-03-25)

### Chore

* chore(CI): Update semantic-release config

- no pre-releases anymore ([`d1b4b86`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/d1b4b862694b844db746c90e4280dd73ecbb9c7b))

### Fix

* fix(notebook_utils): notebookapp import path changed ([`27266db`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/27266db0c62a1e35be8bfb90194b001f29d4534c))


## v0.1.6-dev.5 (2023-04-20)

### Chore

* chore(Packaging): switch from test.pypi.org to pypi.org ([`7878db8`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/7878db88d36156eefa1c4db807fa3a17e82ea755))

* chore(GitHub Action): Updated templates ([`ff82de6`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/ff82de6b3ccd06fd5bd8b3728215b901f8a74c39))


## v0.1.6-dev.4 (2023-04-20)

### Chore

* chore(GitHub Action): test first, continue on success; some fixes

- reapplied cookiecutter ([`ac9f279`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/ac9f279c68570c31d9b478f3e988e503b30549af))


## v0.1.6-dev.3 (2023-03-28)

### Chore

* chore(GitHub Action): Remove old doc files first before populating with newly generated docs ([`d828528`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/d828528266cd219b9bc4804e2fdb9ad51842cc97))


## v0.1.6-dev.2 (2023-03-27)

### Chore

* chore(GitHub Action): fix update of gh-pages ([`c74f6ba`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/c74f6ba5c4c557cf20d236ee848f31179f75e29c))


## v0.1.6-dev.1 (2023-03-27)

### Documentation

* docs(analysis): minor fix ([`601a6f7`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/601a6f7dbbf383810add39620748808c51af6fa3))


## v0.1.5 (2023-03-27)

### Documentation

* docs(cleanup): removed obsolete module doc, replaced by autosummary generated files ([`c0d4256`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/c0d4256a5bcbb83a9a9c0ca0dd3001b9d111cb4b))

* docs(format): fix formatting with black ([`5de80d4`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/5de80d4d528bfb2bf106fa38d2cd8f30f6421f19))

### Fix

* fix(reBin): module renamed to binning, fixes name clashes with docs gen ([`ec959fb`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/ec959fb9e1b51d69cdceaf7784b27df22aa6f4d4))

### Style

* style(format): fix whitespace and quotes with black ([`b0b7dba`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/b0b7dbaac59528ead6c663165c8d4dab3aabcdfe))

* style(binning): fix quoting by using black formatter ([`61603f7`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/61603f7de8640437ccd277faefc2d31fa1e1e232))


## v0.1.5-dev.2 (2023-03-27)

### Chore

* chore(Packaging): coveragerc removed, now in tox.ini ([`01a15c1`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/01a15c186d661ca27f6b35d19ee6bfc03468b50e))


## v0.1.5-dev.1 (2023-03-27)

### Chore

* chore(cookiecutter): changelog filename changed ([`f233036`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/f2330369ac49bc958067154684c0d5fe612e190a))

* chore(cookiecutter): updated config &amp; version numbering, pytest cfg, black fmt ([`ffd69f6`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/ffd69f65d1b3012ed3d1a0031bf498c9f4b0f911))

* chore(GitHub Action): reordered to run docs and tests in parallel ([`1beedd7`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/1beedd7753ca3b88d510a15536c53e6049ebc4f7))

### Documentation

* docs(General): config updated by cookiecutter

- changelog in markdown fmt
- readme: some badges replaced by one for ci-cd ([`6c9ddfb`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/6c9ddfb9777cb344378f5a0d86e204dc016a2068))

### Style

* style(config): string normalization, double quotes ([`e8edbc4`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/e8edbc437b3c6876fae1ff72ad24edbcbe82a8f8))


## v0.1.4 (2023-03-03)

### Fix

* fix(readme): license link ([`f98f736`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/f98f7362dd0278210894f138dd7646c8bc92cc9f))


## v0.1.3 (2023-03-03)

### Chore

* chore(Package): updated cookiecutterrc ([`822ed3d`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/822ed3de8a366644a7285c86facc664d787a7361))

* chore(Package): cookiecutterrc ([`203a5cc`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/203a5cc91f83d740b141dc91b9e93b9d25690c90))

* chore(GitHubAction): consistent variable name for documentation URL ([`587eae9`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/587eae98b3770975e6bb31de09733d630cea997a))

* chore(Package): project URL updated ([`d9cefee`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/d9cefee978ff4a4a3d0a195ea1d3d4802b3a7bdc))

* chore(GitHubAction): docs are not build in a matrix anymore ([`4b584ed`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/4b584ed5fa0771c2b381cc35f284018f705ccce7))

* chore(Package): add .cookiecutterrc ([`0101f9d`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/0101f9d19249052dfe29cf2889bffcaf2066b471))

* chore(PythonPackage): remove obsolete tbump config ([`7a4af2b`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/7a4af2b183405bcf5df6874154bb6a9c0bc5fa10))

* chore(PythonPackage): moved ignored .DS_Store to MANIFEST.in ([`cf01d72`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/cf01d72028dc1655f59fea084824417dde703ec3))

### Documentation

* docs(readme): adjust version numbers in readme as well ([`5700694`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/57006942e6625faf9f36dca1bac0719706b4d000))

* docs(readme): using test.pypi.org links ([`240e58c`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/240e58c87ef0cf0dc3d195f237a09c8e8a717e75))

* docs(Package): update project description ([`704a0b5`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/704a0b50a727ef36f685d27ce068103ffa60ca99))

* docs(comments): add some, remove obsolete ([`efe2689`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/efe2689707f410a18cce331f9cd3732fa2190640))

### Fix

* fix(tox): clean env ([`0135426`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/013542651eb2bd9a7e2d3b2e8ef837c38501b578))

* fix(Package): cookiecutterrc updated ([`7b29a17`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/7b29a1764f972379086abb51194604423c9714f2))

* fix(tox): cleanup env removed pckg build files ([`ecd8648`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/ecd86485ec0fe67f646d06ca134fe97310f7a3f5))

* fix(GitHubAction): migrate to pathlib.Path in template rendering ([`d3ae5db`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/d3ae5db8f657e929f4139bb17bb746f7b03961d3))

### Refactor

* refactor(docs): config adjusted by cookiecutter ([`84e00f0`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/84e00f061bc5780a0b3457ec95847b266dcfa2cc))

* refactor(metadata): update project meta data ([`9d6982c`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/9d6982c960fef68b4c155d05162491f2b6e8b4d0))

### Style

* style(pyproject.toml): use double quotes ([`8f902a2`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/8f902a25b0578babc6e2ad3b72cc7adff94361e2))

### Test

* test(tox): find sys Python version when generating files if not specified explicitly ([`e690193`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/e690193e2a7f3f34dd8457b459c82ec1b9643e0e))


## v0.1.3-dev.4 (2023-02-28)

### Chore

* chore(PythonPackage): removed obsolete setuptools requirement ([`a479484`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/a47948497cba680b6a8ccdaf1fa48c4bd5d0878b))

* chore(PythonPackage): removed obsolete version number script ([`84a1309`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/84a1309702f361cc6ebae72047cd68b8d4316d69))


## v0.1.3-dev.3 (2023-02-28)

### Chore

* chore(GitHubAction): jinja macro for setup_python() extended

- for using it in tests workflow as well ([`7dbf684`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/7dbf684ae95f5864970149407de5dc079d1ad63e))

* chore(GitHubAction): docs adjust package version correctly ([`1a50e88`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/1a50e88b5ee40e84a8bf960179907a585921ccb9))

* chore(GitHubAction): fix whitespace ([`1cd8b58`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/1cd8b586b2b7d94ca09c711d0f7287ef726f3d3d))

* chore(GitHubAction): fix YAML syntax

- of generated workflow files
- according to yamllint ([`d5a6ef6`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/d5a6ef684adeaba5bfe001041c7399d7774c2ee1))

* chore(GitHubAction): fix indentation of job steps ([`cff1019`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/cff1019d7d9cd91a7265b32b10a99a98d011104f))

* chore(GitHubAction): jinja macro pip_install_req() ([`2f0beb3`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/2f0beb397bc389c78c9ca641a07f9f6ca8488fcd))

* chore(GitHubAction): removed obsolete job step ([`973497b`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/973497b4e42c82ecbff8c846ce029077b787268e))

* chore(GitHubAction): fix indentation of job steps ([`31b7044`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/31b70440d89eba31c69130bffe2f0d79a81f87b9))

* chore(GitHubAction): jinja macro setup_python() ([`37d1b57`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/37d1b57e1a4baf21a2b6c2bd74bd3d8b677514a3))

* chore(GitHubAction): jinja macro for recurring step in workflow ([`affb68a`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/affb68aa8bce79dbd7fc1dd2e3cd5f6dd315dde6))

* chore(GitHubAction): rename bootstrap script

- better reflect actual purpose in updating github action workflow files ([`e732926`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/e7329260ae4cfd8a62d207538d89b213ac590505))

* chore(GitHubAction): reordered job dependencies

- build once tests completed, docs need current version number as well, which is set by build job ([`0c9ef01`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/0c9ef01d19953d2ce724b858ace98626ca762486))

* chore(GitHubAction): remove debug output ([`2fb6b01`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/2fb6b0112892f6d5d2be6731c7df5e18e9de1e17))


## v0.1.3-dev.2 (2023-02-27)

### Chore

* chore(GitHubAction): debugging build job ([`9eac568`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/9eac56850155cb0ce7eb41a4c0c384e7295d0d62))


## v0.1.3-dev.1 (2023-02-27)

### Chore

* chore(GitHubAction): debugging build job ([`ad8b345`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/ad8b345e049a001c82126babf0e3157088fa8892))

* chore(GitHubAction): debugging build job ([`650ca39`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/650ca3918306c6067012ee21d5eea009629edf09))

* chore(GitHubAction): debugging build job ([`6f95e37`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/6f95e3713fcc85e32c76c3734adc9fd6f03c70cf))

* chore(GitHubAction): debugging build job ([`94b0884`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/94b08845ed943cc1de2851769daf66fec3f9c98d))

* chore(GitHubAction): debugging build job ([`6c2c83e`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/6c2c83e9131e5079d65a6669c68fe3a5ed4597e2))

* chore(GitHubAction): set prerelease version numbers in build job ([`971957b`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/971957bcd0a5b132938d6c7d67dc85f0f7325415))

* chore(GitHubAction): debugging build.release job ([`b727904`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/b727904ff733e05af25929056687302fdf79b762))

* chore(GitHubAction): *runs-on* added to build.release job ([`50e0c0d`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/50e0c0d559d4674f6dcebc5fcdba20bdc5c5aaab))

* chore(GitHubAction): semantic-release with conditional prerelease ([`ee41ded`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/ee41dedd86a172b856f3c1e6983143b2d9fec643))

* chore(GitHubAction): fix coverage badge ([`cf3e73b`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/cf3e73b4963135957c42430da2507bcfd148636b))


## v0.1.2 (2023-02-24)

### Documentation

* docs(distrib): generate entries of submodule *distrib* ([`c8055c6`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/c8055c65ac1d49a757ee30f9cd34fc18e8445944))

### Fix

* fix(Documentation): doctest format in *distrib* ([`5942972`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/59429724fd41e62c7717fa185e7f5c5c1e5b50d9))


## v0.1.2-dev.1 (2023-02-24)

### Documentation

* docs(utils): generate entries of submodule *utils* ([`762a548`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/762a548a967cf54aed7a58f9d84e4cf6e98e25f7))

### Unknown

* v0.1.1 ([`738fdd4`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/738fdd44b27881360f51f540f28cda4aed2e9005))


## v0.1.1 (2023-02-24)

### Fix

* fix(docs): allow markdown format in changelog ([`593356b`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/593356bb0fb6ea7a6c028b99032ed9742708cb6b))


## v0.1.1-dev.5 (2023-02-23)

### Chore

* chore(GitHubAction): use tox to build the wheel for uploading ([`db60a37`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/db60a3799124f252bb532dbc576f2f0dc0e784d5))

* chore(docs): show git commit id in footer ([`b4dc6cb`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/b4dc6cbc15f189cd1fa5d47024199dbb333a9bb4))

* chore(GitHubAction): simplified docs workflow ([`46f65f3`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/46f65f3d1ce33d7b7b0919c996a8c3aa22e56316))

* chore(tox): updated tox config for building wheel ([`97a4306`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/97a43062ed59027d52522e72a20f439b2c6222aa))


## v0.1.1-dev.4 (2023-02-23)

### Documentation

* docs(readme): updated links and badges ([`2e0329d`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/2e0329d510bb5c090d093818c0536993c6292a8a))


## v0.1.1-dev.3 (2023-02-23)

### Chore

* chore(GitHubAction): split up tests workflow to apply dependency on coverage ([`0b66897`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/0b6689765f4e43a8c0c6216489fbe53218479945))


## v0.1.1-dev.2 (2023-02-23)

### Chore

* chore(GitHubAction): fixed workflow dependencies ([`335b82f`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/335b82f8ba9637c9a16df8401918da444fc17d4d))

* chore(GitHubAction): typo fix ([`d730a0f`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/d730a0fa858424b2a68525aa26210ca58a144b55))

* chore(GitHubAction): separate test workflow, put under main *ci-cd* workflow ([`e92f8d5`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/e92f8d598b3664e66a7819a5a51010a88b980d2a))


## v0.1.1-dev.1 (2023-02-23)

### Chore

* chore(GitHubAction): test pushing prerelease version numbers ([`802f015`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/802f015b75dccaf576855d913c026ba807296088))

* chore(GitHubAction): set git identity for creating a tag ([`1c0339e`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/1c0339e68315aa7a147c4a2ef78f9bdb3b403bb5))

* chore(GitHubAction): obsolete job for debugging removed ([`4cb55d7`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/4cb55d7ce677cf7014cd005f654a40bb118922c8))

* chore(PythonPackage): running semantic-release on build ([`1ddd27e`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/1ddd27ed362c47f7023343405692ff7b8570c7a4))

* chore(GitHubAction): remove debugging for secret handling ([`5cc8879`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/5cc8879a860284d2635916e2130aef750a63ee08))

* chore(PythonPackage): prerelease suffix changed to *dev* ([`ad616ce`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/ad616ce57ad2fe56262c98bcef0077d4f72734ec))

* chore(PythonPackage): git sha suffix not supported version numbers at pypi ([`5cd5d07`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/5cd5d073ddcf6530484ba2d3733041ade2499e71))

* chore(PythonPackage): comment on version numbers added ([`831bf8a`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/831bf8a03639bd6a1e3a376c6cb7b7ee2a27bc87))

* chore(GitHubAction): debugging twine credentials ([`601021a`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/601021ad834662bf096442837db41f50d35edc94))

* chore(GitHubAction): debugging twine credentials ([`8745ee1`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/8745ee140d7e6f5720afe51c836b7fc2e0d439ed))

* chore(GitHubAction): debugging twine credentials ([`096a205`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/096a20566d9d32df271a48122a3827e12366f514))

* chore(GitHubAction): debugging twine credentials ([`80284e1`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/80284e16c83b115c6dcf6ddec66a98fa6af697d4))

* chore(GitHubAction): debugging twine credentials ([`24e73b5`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/24e73b5d9f5c0fa4f48ab15d8d62d417cb71e2b5))

* chore(GitHubAction): debugging twine credentials ([`d53c227`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/d53c22759925704bc64068c39f15f8e04aeccb55))

* chore(GitHubAction): debugging twine credentials ([`0df6cbd`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/0df6cbd14b7dbb803ccd56d3ee22cef6b783d0ee))

* chore(GitHubAction): debugging twine credentials ([`d92e306`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/d92e306b8aef200c0f624a840d002ca50126458b))

* chore(GitHubAction): test on ubuntu only, for faster testing ([`1a3ba26`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/1a3ba26ca02c543ea995fda969db644f42482ae4))

* chore(GitHubAction): limit python versions tested for faster processing ([`b23d7a4`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/b23d7a427fede257d0a4215d8da90f6bfaf1c3b8))

* chore(GitHubAction): publish job needs to install required packages ([`3228704`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/32287049c687dc4f8d095bddf7907a086562dcfe))

* chore(GitHubAction): publish job needs to check out repo ([`e871aaf`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/e871aaf76f73ef206fce7e736125a72bcd6dfaa1))

* chore(GitHubAction): syntax fix ([`6474942`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/6474942c2639d9747e2bd1e7dda7cdc4e5275d11))

* chore(GitHubAction): setup Python for publish job ([`bb46163`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/bb46163effa97ab35916b3efeda9eef7b15e57c9))

* chore(GitHubAction): set dev version number before generating docs ([`660076c`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/660076ce25f1cba798857653d3c642ffb958323e))

* chore(GitHubAction): debugging twine credentials ([`8db6a32`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/8db6a32dd02e29ea2b3da853bc42b1e140066c81))

* chore(GitHubAction): debugging twine credentials ([`887b96c`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/887b96c2ca71cb281fd1ef0eec6db68a2ef6da60))

* chore(GitHubAction): debugging twine credentials ([`c09fbf8`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/c09fbf8cfd0441d90ec09fab257c13521d5da4b2))

* chore(GitHubAction): debugging twine credentials ([`52e76d0`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/52e76d003735747f45d0a8a575901109187b2069))

* chore(GitHubAction): moved build dependency to requirements file ([`843bd12`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/843bd12446fb2362d7967c2e5551125dcc005e10))

* chore(GitHubAction): moved build dependency to requirements file ([`803fd94`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/803fd94f71b9c74f33c5f430c91447f24830ec0a))

* chore(GitHubAction): typo fix in twine cmd ([`7ae601c`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/7ae601c54167e2caacc458a1758bcbb91a34b3f2))

* chore(releases): version config updated ([`eb2d5fe`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/eb2d5fee7e75ec371e3b2772534a121c3d0112e2))

* chore(GitHubAction): updated twine config ([`bfec290`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/bfec29095658b5ef0fee84c47a2a8f1527944de7))

* chore(releases): config for semantic-release ([`11452d3`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/11452d39090633242455fe1b8cbfe40de41839a2))

* chore(PythonPackage): removed setup.py, obsolete ([`d6f2aed`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/d6f2aed7653e47ff223186daf64afb884225f4be))

* chore(GitHubAction): install twine before using it ([`6561d70`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/6561d70a30128acc987d39294a8a4360ae7582a6))

* chore(GitHubAction): calling twine directly for uploading to pypi ([`2c7b2da`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/2c7b2da264fc1a6aaaeb6187145263cc3a5e1ab6))

* chore(GitHubAction): fixed build workflow ([`be22d37`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/be22d3743caa5d74ea6859eba147b9c2ab3a094b))

* chore(GitHubAction): fixed build workflow ([`6003c4e`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/6003c4e0a697c3efbc917102ee400440d275feda))

* chore(GitHubAction): fix to swap quotes ([`5fed8f8`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/5fed8f8e521b9b700f0ab3a00182ebef1dad886e))

* chore(GitHubAction): test if python needs to be setup for publishing at all ([`60afc13`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/60afc13569718cf324ebbccbe3a37352e608cbb4))

* chore(GitHubAction): add required module at the right place ([`c2c8769`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/c2c8769f9b4787c1695985384baa30f29a74fd71))

* chore(GitHubAction): module required for building packages ([`8261466`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/8261466f69c06a38adfadaf81dc47bf93e3d0888))

* chore(GitHubAction): workflow for building packages ([`493d0d2`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/493d0d2f3f85a6c48465610e79a916c329268dc2))

* chore(GitHubAction): upgrade pip in templates too ([`f23f8c8`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/f23f8c8617199e5dc1a5d252e103186c91e1334a))

* chore(githubAction): upgrade pip before installing more deps ([`26295b6`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/26295b66a6c6c992844e622d7d7ecfc80b76a3f1))

### Documentation

* docs(config): clean up version definition ([`c18c67f`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/c18c67fae8852f2acdd79ffe3bcb89aa5821c797))

* docs: removed disabled config ([`3059ff9`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/3059ff9fba6a17b845441cd283c0f498c05beab2))

* docs: disabled incompatible sidebar config with furo theme ([`61959be`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/61959be18f26e304042c21872f50dda23635caae))

### Fix

* fix(tox): removed tox-wheel settings

- tox supports building wheels since v4 ([`cacbfe3`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/cacbfe36af39f613efc4651bed4c8875c80c60c5))

### Unknown

* GHA: show available tox options ([`ccce3b0`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/ccce3b06104f540965bc8b0321e3cc301c826e34))

* GHA: pip cache disabled for testing ([`18371d5`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/18371d53beb662f945b7b4d8ff40b3c70163fbb5))

* added tox-wheel to ci required packages ([`7eae72c`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/7eae72c4a2e977c3efc56b5d9c8da76d67d44536))

* readme: updated badge for docs ([`6e78a50`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/6e78a50e5b9b7c47498cdb7bc3c4a493a1cacfe3))

* GHA reorganized, general python version set in bootstrap ([`ddded7b`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/ddded7b39dc968b38a724eafcb98087c7b113620))

* GHA reorganized, syntax fix ([`8b3c7c2`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/8b3c7c22aac647f5e69c9a586a0f3b431a952f6c))

* GHA reorganized, updated template to current workflow ([`51dce0d`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/51dce0dec931d7f14de6e8471865c07ebc4fdd97))

* GHA reorganized, run docs workflow from main wf only ([`6d2ce58`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/6d2ce585f2f408c44b3fcc8bd7c219b76a06aa46))

* GHA reorganized, little fix ([`692a145`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/692a145559990daf84f7f99e44b1cf1c95a117e2))

* GHA reorganized, moved docs to separate workflow ([`9970f71`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/9970f7105319cf5a8b33744e0f0c88adb17d1bca))

* GHA reorganized, moved docs to separate workflow ([`15b5fe0`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/15b5fe08af9ab4a6ec8095d681315003304ba203))

* GHA reorganized, some fixes ([`677bf07`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/677bf0745dc58c22ca18b84b0a795ee4386ae798))

* GHA reorganized, more fixes ([`aa768a5`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/aa768a55e02f5aefc2be3a6981fafaab3c22b8c7))

* GHA reorganized, more fixes ([`185519a`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/185519a7cd449784d0f60a7c73767666553a2c47))

* GHA reorganized, more fixes ([`48ca3b6`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/48ca3b6748bd289b4539e7a60cf4aa3ee913db61))

* GHA reorganized, fixes ([`4ddab64`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/4ddab64307dde686e62a390dff204a5a887faa82))

* GHA reorganized, fixes ([`fcfeba0`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/fcfeba0fc4877f7f440ec26d1cef2bd8eed86080))

* GHA reorganized, fixes ([`1e89f0b`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/1e89f0b0ae2d6fac9840253cb52bb550d0175a61))

* GHA reorganized, fixes ([`37a6133`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/37a61331786cb134766d9a8cb210695c40363f98))

* GHA reorganized, testing ([`f43f9ae`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/f43f9aefd444a1585df69c72ec44d0db57a95d37))

* comments added ([`af59a8a`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/af59a8a01d7891a35a2c1b9a76f303b5dfb1139a))

* updated GHA bootstrap template ([`0932c61`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/0932c61d27fdee1686256454b45f728c13d2dfa0))

* readme: fixed link to coverage report page ([`1e173dc`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/1e173dc08abec18fb231dc56432bab3b1244b614))

* GHA coverage: fixed report url ([`5f67507`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/5f675073bcb71d004abc79d89d3583232c8073b0))

* GHA debug coverage combine errors: fix path of json file for badge ([`e27d159`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/e27d159829d2a81ee7e9c9f2e720fc71c0bc0bfe))

* GHA debug coverage combine errors: fix path of json file for badge ([`5a2b4fd`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/5a2b4fd5d723137cfdee177a5691e880c83dd67b))

* GHA debug coverage combine errors: fix git add paths ([`308066f`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/308066f8fc00c61a8eaf8a225993dd94f39c5d66))

* GHA debug coverage combine errors: testing GH env vars ([`7939753`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/7939753baad0f9c64783c6019cc6e8475a48159b))

* GHA debug coverage combine errors: test more path mapping ([`9e59c4e`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/9e59c4ebdc73f2831a5343b1ac2baef11e4adbcc))

* GHA debug coverage combine errors: more path mapping ([`67f7221`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/67f722133068fdd0383c2bd4f406ab662bf50366))

* GHA debug coverage combine errors: show stored paths ([`b7f6c9a`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/b7f6c9aea32db8d35876bea468d318d8b9e50d52))

* GHA debug coverage combine errors: show path mapping ([`75d2ea9`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/75d2ea95557727c3117bce691c8f0db738d41f65))

* GHA debug coverage combine errors: handling subdir tests similarily ([`7a8dcf5`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/7a8dcf577a0ada5b20deceedde3cb16c00cec8c6))

* GHA debug coverage combine errors: do not lookup non-existent file, forgot removal ([`dd4a886`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/dd4a88654cd0e2d66212e47e6b9267b6697ec982))

* GHA debug coverage combine errors, abs paths differ between platforms ([`70071de`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/70071def90995145d9244a88971b987aed1cdd8b))

* GHA debug coverage combine errors ([`e6507ed`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/e6507ede7f01997560e02bfa21ac0d64f63b001f))

* GHA debug coverage combine errors ([`4f54c5f`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/4f54c5fc3a3088a80162f4da330247f18700caff))

* GHA debug coverage combine errors ([`51511e8`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/51511e8a32c35725dfe9cec71b557f1aa86686bd))

* GH action coverage: Skip files with no code ([`55cf268`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/55cf268aeedc0d24631358dea64109e491e1e1a9))

* docs env needs toml module for reading values from pyproject.toml ([`6a2d755`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/6a2d7555ce44ff820f3375dca9cd0714a2e54c49))

* applying isort config

- single line for imports from same module, saving space ([`02c6bbc`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/02c6bbc9cd0cd06375bd263efb072d9f0116ac69))

* updated isort config ([`78e38e9`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/78e38e9d298bc384695c9104195f749cdcc6a52d))

* docs config: using urls defined in pyproject.toml ([`33d5f23`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/33d5f2338e3a95212c21396d9007bac1495f30a8))

* moving isort config to separate file, not picked up from pyproject  in a pre-commit hook ([`bfaf1e0`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/bfaf1e0ab5be225e5e4c34ffc8b1ea8bedb59688))

* minor formatting of GH action bootstrap template ([`9f935bc`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/9f935bc5f042766b83aeb70e60312688186842ee))

* pre-commit uses pycqa repo for isort ([`4b4a31c`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/4b4a31c15e9a07455fe9796e17ddbce5f23456ed))

* updated pre-commit hook versions ([`4fdec5c`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/4fdec5c7bab285cb53665d23d063c3ef117ce077))

* docs switching theme to furo

https://github.com/pradyunsg/furo ([`ceab414`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/ceab4148b9fbac53f5ffd936da15f39bedfad968))

* updated GH action workflow from bootstrap template ([`87e1b2b`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/87e1b2bd809295c4c960333a048cc3098355a424))

* Adding upload of generated docs to GH action bootstrap template ([`6337839`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/6337839d317a14d3f2f8989bc8f1615c60fa826c))

* GH action bootstrap template using values defined in pyproject.toml

for documentation url and path to coverage reports ([`f59959d`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/f59959d4c52f868a5f3eeadfe67294026fec75bd))

* moved project meta data from setup.py to pyproject.toml ([`a73f9a7`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/a73f9a7c52df781bffcf388a2e5932573bbc51a7))

* removed obsolete dependency from github action template ([`0d071bc`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/0d071bc80d627395a569d007f05ba26e880ad28b))

* tox: removed coverage combine for single runner, useless ([`831fa6b`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/831fa6b16ac6053dfff570ca3098e4610709b039))

* GH action syntax fix ([`38574da`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/38574da969c6ba1669095a4f5797e5ba9e91f770))

* GH action updated for building docs with an tox environment

- and uploading the build results to pages, replacing old *build_docs* job ([`23c980b`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/23c980b6a90ec71520392684b6a7a7c04db8a97d))

* tox: updated bootstrap template for github actions ([`47528b8`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/47528b8c2705a4f80339561d877f14038ab19691))

* tox: build env for package building ([`91969bb`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/91969bbe7bf7e69f006e439166db2d7ff62a063e))

* tox.docs: generating placeholder for github pages;

- disabled doctests by sphinx which are run by pytest later anyways ([`bcaaa54`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/bcaaa5448d764b7969f1885740b4914df74ed965))

* tox: coverage combine command added ([`bc45701`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/bc45701fc9cf656aa191b2b61df60d10f448be4f))

* readme: removed unused table def ([`9665ccf`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/9665ccf5f5f3d753135dcdf477c09f9212f512eb))

* GH action: cov report directory singular ([`a8f6c8a`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/a8f6c8ae2a1ea3be5b466b042946b089b3244950))

* readme: coverage badge added (from report) ([`6570cf1`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/6570cf1a6c7036a8998536740867819a52ed084b))

* GH action: remove gitignore from reports first ([`ffd4281`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/ffd42815fc0c59943e0e911ced55bde40edb320d))

* GH action: fixing coverage report publishing ([`802b130`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/802b130c1478d5da05079eecdf29a986e0c2022a))

* GH action: missing packages added ([`128b3db`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/128b3dbebde3977b3030606a6517894b14995152))

* GH action: removed some runners for quick testing ([`e9671ca`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/e9671caf4573f6d03f88d06393f69ad3639115b9))

* GH action syntax fix ([`0b0021b`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/0b0021bc087cf39b7209ea98c55736126de70472))

* GH action fix; removed non-exist docs badge from readme ([`86cbbe1`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/86cbbe13540ff4691f2d7d2aa05007d09aacf56e))

* GH action logic fix ([`1b94f49`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/1b94f49a9e27f2c6819b83f6fe0fcd6a465d4b76))

* GH action syntax fix ([`37b182c`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/37b182c3ea20652f39891021e8598a37e218889b))

* fix for GH action for coverage report ([`f05dd01`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/f05dd0134f119b62ee64446e05bcb542ba22b001))

* GH action adjusted for coverage report publishing

- along with documentation in gh-pages ([`d7c36a4`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/d7c36a4e4f2bf4574fe9ab2db2888da926b19ab7))

* tox config format fixes ([`210b5e3`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/210b5e39a37ecdf1abaf083379e05fa8d5e6726a))

* Testing: updated GH actions workflow ([`9a5abf1`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/9a5abf1c2bfc28785ebb54a6d9c25a20635f3fec))

* readme: download numbers from pypi ([`7082226`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/7082226643aef7bcdd4d42d3109653e77fde230c))

* readme: minor formatting edit ([`645e0f8`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/645e0f8f87965e5e42e807bbbb573b861ab7f1c9))

* readme: adjusted badges ([`343dc81`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/343dc812104a84eea4fe028656edb4befaefb8e5))

* updated versions of employed GH actions ([`3061775`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/3061775f58d566fecee64cb78cca33a5957a98d4))

* fixed broken link ([`e41268d`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/e41268d735e8ad78692db43b8581975993946782))

* removed missing tbump.toml from manifest ([`1a54907`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/1a549076017a9608d33b428e750216db8d135ead))

* Dependabot config ([`4578709`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/4578709355e0d4ad839b61f42ff2af01c85ee7ff))


## v0.1.0 (2022-11-10)

### Documentation

* docs: let sphinx use numpy directly instead of mockup

- fixes issues with numpy members ([`9b6ec6d`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/9b6ec6d3f4123b8bfb0934cdb2e8a0df0933daee))

* docs: sphinx extlinks syntax updated ([`0866ee7`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/0866ee71cbfa5b8f1134858a44fe8e360707faec))

* docs: URL updated ([`146039c`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/146039cc13670cfc62ca295935567e14ba38d738))

* docs: fix docs gh workflow spec ([`49d7e93`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/49d7e9305987cb918e3ea3c812c7aeac2fe36c56))

* docs: fix gh workflow spec ([`b977751`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/b97775186b5554a9bf260c6ad34ed63481571eae))

* docs: fix gh workflow spec ([`e23c22c`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/e23c22cae9045a75c7ff41ddffdd44c93fd027da))

* docs: fix gh workflow spec ([`024295d`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/024295d797da7274071cf54085d614a2f8e96a53))

* docs: fix gh workflow spec ([`12adda9`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/12adda94ad39ce9c4e61687cdbf829c196ff81ed))

* docs: fix gh workflow spec ([`f062d12`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/f062d12d3f2cb430c643228573cf76aef31dfee6))

* docs: updated urls and gh workflow spec ([`66a0704`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/66a07049567a524a82633547c8006ed1630238c1))

### Unknown

* tbump config updated ([`e17de91`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/e17de9111659992b9419efc7e07c58172737e285))

* package classifiers and readme updated ([`4cafdca`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/4cafdca402cb8171b7ab32de4c93feeb94e00af4))

* tox: removed passenv=*, more strictness ([`818ffa1`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/818ffa1a590e42aa2599679755ffaeea794d346f))

* moved tbump config into pyproject file ([`b8b9881`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/b8b9881fec80199ec5e730d33fbb5a427acfd9c1))

* isort excludes .ipynb_checkpoints ([`db90f62`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/db90f62015abc54088eae146419863ff9a1c38ac))

* flake8 config updated ([`20a46bc`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/20a46bc9ca8d09f79795d10b91ee759042045f08))

* reformatting according to pre-commit config ([`54fd524`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/54fd524c6791ec3ac6a7f95a153bf739c35bf8d1))

* tox:check: let check-manifest ignore macOS meta files ([`d301bd2`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/d301bd2d02d5030e7c50071187bb6f4ea895c63e))

* gh: removed obsolete testing.yml ([`1ce898d`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/1ce898dfc5c547bbef27e159cc377478f26d39d5))

* readme: updated badges ([`790bf44`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/790bf44e76f1f25959672536cbe6c588efe2ac17))

* readme: updated badges ([`99ddde2`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/99ddde2155dab5bbda3b632d58576a85f3dbf701))

* readme: updated badges ([`f18418c`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/f18418cc52850c6622c4cc0ab6ceb01f4e4839eb))

* readme: fixed badges, renamed testing -&gt; tests ([`3efb28f`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/3efb28fdfbef47fd6a776fada5a7f0b8804a4fa7))

* removed pypy test environment from github actions ([`17f8515`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/17f8515fda7746b6c43e4e2ff94fedce95e9a2ae))

* removed pypy test environment ([`e2cfa0a`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/e2cfa0adbfdf3b3d927949a5f43e37ae1367911a))

* conda_environment.yml not needed anymore ([`b28806f`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/b28806f0f8aa7faa60b6162b05a84386e72e4f1c))

* tested testing config, enabled doctests ([`a273d9d`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/a273d9d218ca151f19623fd7b978557e23a55ea2))

* generate github testing workflow with tox ([`f04bb7b`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/f04bb7bae96a417d56d545be61423930a210fa4a))

* tox:bootstrap: don&#39;t fail for macOS .DS_Store files ([`0445011`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/0445011ea7721471aa6caee06565062d041a6110))

* tox setup added and works partially ([`4956d25`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/4956d2573999ed7fd5aeb5dc8f22b99ef5e6c6da))

* moved implementation to src subfolder ([`a917c30`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/a917c30fbfabd5f14666b36305484f3d8dee8cd6))

* updated gitignore ([`2499639`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/24996396b32b4991cfb9450e028f0d73b3fff138))

* readme: updated docs gh workflow badge ([`3bb0b40`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/3bb0b40ffd5c95869151efa5274e1b4e9bc5ec60))

* documentation setup ([`fa494d0`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/fa494d05c78ec8ccd6d98caedd0c67479bc301bb))

* editorconfig added ([`61299aa`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/61299aa1904401865aa169112acdada96d29f5fe))

* pre-commit config added, running reformatter, import sort and flake8 linter for the first time ([`0537b68`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/0537b68cc3e139911e7b65b2bb4d72ca9d85dac9))

* let git ignore macOS meta data files ([`6e35aa3`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/6e35aa33bbacb4bf3a2dc041c59aee17ae793f13))

* distrib: removed radius-specific scale factors when converting (LogNorm) distribution parameters

- adjusted doctests
- changed float formatting to cover broader value range ([`bf7bcca`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/bf7bcca230d1d3aeb0c3aea41035b71180d33a01))

* distrib.Distribution.xlabel added

- flexible subject of distribution
- allows description with units for plots
- removed radius-specific labels ([`30ad6c1`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/30ad6c138545afb08f1c68466405f8dd09d0cfab))

* indicate python raw string to protect LaTeX commands ([`4483cb5`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/4483cb525b50aa04a5f9105a1910e333880e3110))

* utils.setPackage() prepend local module search path ([`247973a`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/247973af69237825dd8f4def2accef20b2941c47))

* distrib: handling logNorm params *distrPar* as dict now, doctests added

- in favour of pandas.DataFrame conversion
- changed input/output format of distrPar… helper functions ([`0aad717`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/0aad7179132ec90f715badd0f89e99adb86e7016))

* readdata: fixed imports, allow disabling info output by *print_filename* arg ([`aa1cf22`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/aa1cf22f9af49db58a43be7feaf76206d6a84af5))

* readPDH replaced by a pandas.read_csv wrapper

- readPDH corrupted data before by replacing the uncertainty column by the a copy of the first column read in ([`9d3c6a4`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/9d3c6a45b5875e45289d6678695b2cc3d387cbfb))

* fixed __init__ ([`55e9d20`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/55e9d20dc75fad8e73c459a96d351043ace693f4))

* readPDH: detection of XML section updated ([`096521f`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/096521f678ca4c8e42161b2b59550a0f8cc636e3))

* gh action: enabled testing on all platforms ([`45e203c`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/45e203c73bcba0eca42cf02d2a9e129f0702b826))

* gh action: testing the latest python versions ([`452ec3d`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/452ec3da6bc015e64e63549e0a0a8566fe041c9c))

* gh action: removing debug output ([`6f75e48`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/6f75e48313946fb407d136c9eca65abad2adec70))

* gh action: testing conda environment setup ([`6644b09`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/6644b093b7332fec4bd0918b977e3f3b10bc7956))

* gh action: testing conda environment setup ([`58f318c`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/58f318c9fe2d6b66a80440bff6d95427d0934b09))

* gh action: testing conda environment setup ([`46bd4e0`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/46bd4e0d7811da2b5835485ed522fb3a956b1b72))

* gh action: testing conda environment setup on a single runner for now ([`94baf5b`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/94baf5b8f32fb3294204e346c520cc777cc2fb8c))

* gh action: setting up conda environment ([`01aeaae`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/01aeaae78e08a0ed1e6df32d92d101f778c8b982))

* gh action: setting up conda environment ([`003e018`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/003e01878d9f4c79b7da7c8d15fe50fe31c410a5))

* gh action: investigating conda environment ([`4f89ffb`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/4f89ffb3288f4a3e6c95bad031857f3593937bb6))

* updated GitHub Action ([`7844e90`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/7844e90b2457dea869fa96cdd9b1d1e5f341439f))

* utils: moved jupyter notebook related helper to separate file/module

- avoids unnecessary dependencies elsewhere ([`4bbee4e`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/4bbee4ef4dde0a8591215afdd527f74f9b44d303))

* testing workflow runs doctest on utils module ([`6d19fd4`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/6d19fd4a2bf9dd1250707bc5b02f8d375865aff3))

* utils.isList(): doctest added ([`f27855d`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/f27855dff40990b98a901d0f8d0f7981deae3332))

* testing workflow: fixed python versions ([`a71e60e`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/a71e60ea8173d0549b8f8bfd3e9d03d93dab52e8))

* defined new github action for running tests ([`3589299`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/3589299bd25d5c9e7822fb96a9f73badb43d39f1))

* Distribution.uncertRatioMedian() added ([`8a2ef2d`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/8a2ef2d44237c33c617cad02ce16309b1984f648))

* distrib.getLargestPeaks: fixed sort order of largest peaks ([`9cca28f`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/9cca28f442a75bba1097c670ab3c3c10d6578fa2))

* show LogNorm params for each peak ([`64b60e7`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/64b60e7094ff980dd8eba0a12e83fa1dd5f4ef4c))

* introduced distrib.Distribution for finding and plotting peaks ([`6beadf3`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/6beadf3ae55330ec5ec362263f2afef449fa0080))

* analysis.getModZScore() calculates the modified z-score of some data arrays ([`2250a59`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/2250a59f4aca728ccf79b041b5e148835afb3182))

* distrib.findLocalMinima: skip peaks with less than 5 points

- unlikely to contain additional minimum ([`712d590`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/712d5904218beb9e129d30fb7f6dedb84e050175))

* distrib.findLocalMinima() fail gracefully on single peak ranges

if it can&#39;t be fitted ([`45eb76b`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/45eb76b5ab67ad0d190c88ff4e6846e16e446994))

* plotting.GenericResult with x-axis label ([`1a14688`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/1a1468808a0fb0458a6b8a06051ec6dcb7434edd))

* missing numpy import ([`8c01e86`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/8c01e86c26f0c1a500ad21174189fba1ffb08836))

* added plotting.GenericResult ([`96cf6c8`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/96cf6c8f7062fce9b83404e3f86658d6a9e73bc4))

* distrib.normalizeDistrib: convert pandas.Series to numpy.ndarray first ([`a50f78e`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/a50f78eded5f12f3204a25046b3b6f4ed6164562))

* distrib.findLocalMinima() added

- separates multimodal peaks reliably ([`0ac94c7`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/0ac94c760f93bfa53bc823d1ccec8901eb5af306))

* distrib.findPeakRanges() filters monotonously increasing/decreasing &#39;peaks&#39; (artefacts) ([`7b967c0`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/7b967c00772bea6adce2e735d9c4f54bc1e70d18))

* distrib.distrParFromPeakRanges: convert pandas.Series to numpy.ndarray at the beginning ([`bb19270`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/bb192703cece3027d5766f66c8c5a9c27f61df32))

* distrib.test: fixed indents, replaced tabs by spaces ([`da8f402`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/da8f40236fd5906bbc8c28a36ce8eadd1f2b8c36))

* plotting: increases limit for warning about many plots ([`ef8a6fd`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/ef8a6fd7ff86941eef5f45af38d644a1a048bfef))

* plotting.plotVertBar() now with kwargs being forwarded to matplotlib ([`35dbce1`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/35dbce14a89472aa121483ab96078bcd9270d9f7))

* utils.updatedDict() added ([`03fe42c`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/03fe42c0702efb7a49493c96f4d5768f72c8e86f))

* isList() moved to utils ([`4367a6c`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/4367a6c2c1245a5c3cfb071afd3bccdd96591cb3))

* datalocations.getDataFiles() argument handling lists and non-lists ([`4ee348a`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/4ee348a8f5caebac6f4c4009e5f999abe05237a0))

* datalocations: filtering file names with in-/exclude patterns ([`d65efff`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/d65efffa2df938033443ba54fa09570eaf4afbc3))

* datalocations.getDataFiles() with filename pattern argument

- removed DLS specific file extension matching ([`7d10c9c`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/7d10c9c237f8b48a9c6b8ced05a7bb92c2016ec8))

* plotting.createFigure(): fixed argument ([`ba6ae3b`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/ba6ae3bc2e1ddde3fdda9b9e0bc02b58dcf2ed6b))

* added modules for plotting and distribution helpers ([`3472db8`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/3472db8e9217c9ae0fa1bb3a078e0af04d3328cb))

* utils.fmtErr() ([`56457ae`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/56457ae8a37ff474165c2c9959e115f8c341c48c))

* utils.grouper() ([`a5ad6aa`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/a5ad6aaf80c1dc6be417fd20c22c84c93046dd88))

* utils.setPackage() added ([`969aae8`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/969aae82848b53a0d6257877011dc89e3eb10852))

* datalocations module added ([`f4fb7ff`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/f4fb7ffd0dcc2eab2319e257d0c8dca5be1d6d75))

* utils: OS helpers and for 7-zip added ([`629c0fa`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/629c0fab2e2a9012b76e069ed199107ab6e2e179))

* utils.setLocaleUTF8() added ([`8dc76f3`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/8dc76f3be20b754df2631a6655fc5918ceed72d3))

* minor: line endings converted to UNIX style

(default for jupyter and notebooks) ([`45d3535`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/45d353595dcbfdc864a02225475532c4d7825d22))

* reBin: removed unnecessary whitespace ([`65e622b`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/65e622bae6f73eef4f4d3f946ec038c33e97d50c))

* reBin: show help when called without arguments or files ([`1c8244c`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/1c8244cbfbbfd1373254069bb04062f3e6baeee0))

* reBin: fixed python3 compat. ([`05468c0`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/05468c0784d33fc8e8ecea686f06d0216e7f7aa7))

* disabled nbstripout checks

- jupyterlab git extension handles cell output fine now ([`8835ff0`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/8835ff05cf91c42c470c7f572da8af179a9b8866))

* license added ([`10bb685`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/10bb68573b9b2dd66370bd8bf277d0aa9e354724))

* git: check if installed at all ([`80e7328`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/80e73289d376d18ca7ae135e4ae3d0249a724bf2))

* handle exception if git submodule is moved out of parent repository ([`fb382bd`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/fb382bd3508c8c35aa796b89e765220280cec6c1))

* added showBoolStatus() to pretty print the value of a boolean variable ([`b00316c`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/b00316c60cd5036750104961e7c10337df5a451a))

* added PathSelector in *widgets* module ([`189b56e`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/189b56e1a0af30876013bf676577c2bd4d9e1183))

* git: using full python path for running nbstripout during checkRepo ([`1fbe3cc`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/1fbe3cc93f778f69dc34e569fc54d0906268357a))

* set git status text always transparent ([`9e5943f`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/9e5943fac800ff3385cc2ebb058d3c95608533a0))

* git: partial transparent git status if repo is clean ([`b2fc0e9`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/b2fc0e9e1020c1fcd36cb2a35ab3edd6cc50feb3))

* fixed git module: using subprocess instead of ipython syntax &#39;!&#39; ([`95e7851`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/95e78510aaba7ceeab4515b226f8aad486140424))

* functions for git repo status added ([`4c1f620`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/4c1f6201707e3bb5591614eae102b8e63abf4972))

* fixed encoding header info ([`8375642`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/83756420fab8f3851ce881f54744a2caba20e19d))

* use proper boolean operator ([`94fc592`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/94fc59229261b4acf8e6f32027a4649f133291ad))

* diff.textconv and filters for IPYNB and XLS files ([`ec97ca4`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/ec97ca423a0353c0d82c4c77b141f3a14602e8c8))

* added pycache to gitignore ([`7650b60`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/7650b60079190303a1570caaa3c8016ecd74dd92))

* fixed module path ([`e7f866a`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/e7f866a13044a5b064f3b94bfa8cb15159ea9af3))

* removed Jupyter startup scripts, not needed here ([`c0e07b0`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/c0e07b0675efe51dff549f7526371947b76e8bff))

* init file to make up a proper python module ([`7b984da`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/7b984da192d03a586941374755514f5b11515bf2))

* small-angle scattering data rebinning routine by Brian Pauw ([`eae62d8`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/eae62d8f317b19d3b3022ba6285df0df4ecd1f9b))

* code for parsing a PDH file ([`af59678`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/af59678ff824dfade45b8c18b83ee390b1f14413))

* Jupyter shortcuts added ([`85a8b9b`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/85a8b9b6c85065fa1d4491efbf479973e4c8e238))

* Initial Commit ([`645ef06`](https://github.com/BAMresearch/jupyter-analysis-tools/commit/645ef06938f90d3219c17f74c23d9e610c5a1753))
