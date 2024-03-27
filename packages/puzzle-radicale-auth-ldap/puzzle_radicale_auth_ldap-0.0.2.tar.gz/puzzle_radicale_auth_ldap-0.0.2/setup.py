#!/usr/bin/env python3

from distutils.core import setup

setup(
    name="puzzle_radicale_auth_ldap",
    version="0.0.2",
    description="LDAP Authentication Plugin for Radicale 3",
    author="Raoul Thill",
    license="GNU GPL v3",
    install_requires=["radicale >= 3.0", "ldap3 >= 2.3"],
    url="https://github.com/puzzle/puzzle-radicale-auth-ldap",
    download_url="https://github.com/puzzle/puzzle-radicale-auth-ldap/archive/refs/tags/v.0.0.2.tar.gz",
    packages=["puzzle_radicale_auth_ldap"],
    python_requires=">=3.6"
    )
