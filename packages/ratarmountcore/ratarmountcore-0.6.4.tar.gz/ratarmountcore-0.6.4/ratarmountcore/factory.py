#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import traceback

from typing import IO, Union

from .compressions import supportedCompressions, checkForSplitFile, rarfile, zipfile
from .utils import CompressionError, RatarmountError
from .MountSource import MountSource
from .FolderMountSource import FolderMountSource
from .RarMountSource import RarMountSource
from .SingleFileMountSource import SingleFileMountSource
from .SQLiteIndexedTar import SQLiteIndexedTar
from .StenciledFile import JoinedFileFromFactory
from .ZipMountSource import ZipMountSource


def openMountSource(fileOrPath: Union[str, IO[bytes]], **options) -> MountSource:
    printDebug = int(options.get("printDebug", 0)) if isinstance(options.get("printDebug", 0), int) else 0

    joinedFileName = ''
    if isinstance(fileOrPath, str):
        if not os.path.exists(fileOrPath):
            raise RatarmountError(f"Mount source does not exist: {fileOrPath}")

        if os.path.isdir(fileOrPath):
            return FolderMountSource('.' if fileOrPath == '.' else os.path.realpath(fileOrPath))

        splitFileResult = checkForSplitFile(fileOrPath)
        if splitFileResult:
            filesToJoin = splitFileResult[0]
            joinedFileName = os.path.basename(filesToJoin[0]).rsplit('.', maxsplit=1)[0]
            if 'indexFilePath' not in options or not options['indexFilePath']:
                options['indexFilePath'] = filesToJoin[0] + ".index.sqlite"
            # https://docs.python.org/3/faq/programming.html
            # > Why do lambdas defined in a loop with different values all return the same result?
            fileOrPath = JoinedFileFromFactory(
                [(lambda file=file: open(file, 'rb')) for file in filesToJoin]  # type: ignore
            )

    try:
        if 'rarfile' in sys.modules and rarfile.is_rarfile_sfx(fileOrPath):
            return RarMountSource(fileOrPath, **options)
    except Exception as exception:
        if printDebug >= 1:
            print("[Info] Checking for RAR file raised an exception:", exception)
        if printDebug >= 2:
            traceback.print_exc()
    finally:
        if hasattr(fileOrPath, 'seek'):
            fileOrPath.seek(0)  # type: ignore

    try:
        if isinstance(fileOrPath, str):
            return SQLiteIndexedTar(fileOrPath, **options)

        return SQLiteIndexedTar(fileObject=fileOrPath, **options)
    except RatarmountError as exception:
        if printDebug >= 2:
            print("[Info] Checking for (compressed) TAR file raised an exception:", exception)
        if printDebug >= 3:
            traceback.print_exc()
    except Exception as exception:
        if printDebug >= 1:
            print("[Info] Checking for (compressed) TAR file raised an exception:", exception)
        if printDebug >= 3:
            traceback.print_exc()
    finally:
        if hasattr(fileOrPath, 'seek'):
            fileOrPath.seek(0)  # type: ignore

    if 'zipfile' in sys.modules and zipfile is not None:
        try:
            # is_zipfile is much too lax when testing for ZIPs because it's only testing for the central directory
            # at the end of the file not the magic bits at the beginning. Meaning, if another non-ZIP archive has
            # zip contents at the end, then it might get misclassified! Thefore, manually check for PK at start.
            # https://bugs.python.org/issue16735
            # https://bugs.python.org/issue28494
            # https://bugs.python.org/issue42096
            # https://bugs.python.org/issue45287
            # TODO This will not recognize self-extracting ZIP archives, so for now, those are simply not supported!
            if isinstance(fileOrPath, str):
                with open(fileOrPath, 'rb') as file:
                    if supportedCompressions['zip'].checkHeader(file) and zipfile.is_zipfile(fileOrPath):
                        return ZipMountSource(fileOrPath, **options)
            else:
                # TODO One problem here is when trying to read and then seek back but there also is no peek method.
                #      https://github.com/markokr/rarfile/issues/73
                if fileOrPath.read(2) == b'PK' and zipfile.is_zipfile(fileOrPath):
                    return ZipMountSource(fileOrPath, **options)
        except Exception as exception:
            if printDebug >= 1:
                print("[Info] Checking for ZIP file raised an exception:", exception)
            if printDebug >= 3:
                traceback.print_exc()
        finally:
            if hasattr(fileOrPath, 'seek'):
                fileOrPath.seek(0)  # type: ignore

    if joinedFileName and not isinstance(fileOrPath, str):
        return SingleFileMountSource(joinedFileName, fileOrPath)

    raise CompressionError(f"Archive to open ({str(fileOrPath)}) has unrecognized format!")
