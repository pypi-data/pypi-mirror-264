from icebreaker.versioning import VersionFileBased

__version__: str = VersionFileBased().resolve_version()
