#!/bin/bash

# Script for building Qt WebEngine packages for Chum. Run this script
# in top directory of checked out qtwebengine repository. May have to
# run it with sudo - depending on docker requirements

set -e

RELEASES="4.5.0.19"
ARCH="i486 aarch64 armv7hl"

# either testing or regular
OBS_REPO_BASE=https://repo.sailfishos.org/obs/sailfishos:/chum:/testing

for release in $RELEASES; do
    for arch in $ARCH; do
	TARGET=${release}-${arch}
	if compgen -G "RPMS/${TARGET}/*.rpm" > /dev/null; then
	    echo "RPMs for ${release}-${arch} are found in RPMS/$TARGET, skipping"
	else
	    echo "Building RPMs for ${release}-${arch}"
	    rm -rf RPMS/${TARGET}
	    docker run --rm -it -v `pwd`:/source \
		   sailfishos-${arch}-${release} \
		   buildrpm -v chum \
		   -r ${OBS_REPO_BASE}/${release}_${arch}/
	    pushd RPMS
	    mkdir $TARGET
	    mv *.rpm $TARGET
	    tar zcvf ${TARGET}.tar.gz $TARGET
	    popd
	    echo "RPMs for ${release}-${arch} ready"
	fi
    done
done
