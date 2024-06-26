%global qt_version 5.15.14
%global qt_webengine_version 5.15.17

%global _hardened_build 1

%global use_system_libvpx 1
%global use_system_libwebp 1
%global use_system_jsoncpp 0
%global use_system_re2 0
%global use_system_libicu 1

# spellchecking dictionary directory
%global _qtwebengine_dictionaries_dir %{_opt_qt5_datadir}/qtwebengine_dictionaries

%global rpm_macros_dir %(d=%{_rpmconfigdir}/macros.d; [ -d $d ] || d=%{_opt_qt5_sysconfdir}/rpm; echo $d)

# exclude plugins
%global __provides_exclude ^lib.*plugin\\.so.*$
# and designer plugins
%global __provides_exclude_from ^%{_opt_qt5_plugindir}/.*\\.so$
%{?opt_qt5_default_filter}

Summary: Qt5 - QtWebEngine components
Name: opt-qt5-qtwebengine
Version: 5.15.17
Release: 1%{?dist}

# See LICENSE.GPL LICENSE.LGPL LGPL_EXCEPTION.txt, for details
# See also http://qt-project.org/doc/qt-5.0/qtdoc/licensing.html
# The other licenses are from Chromium and the code it bundles
License: (LGPLv2 with exceptions or GPLv3 with exceptions) and BSD and LGPLv2+ and ASL 2.0 and IJG and MIT and GPLv2+ and ISC and OpenSSL and (MPLv1.1 or GPLv2 or LGPLv2)
URL:     http://www.qt.io
Source0: %{name}-%{version}.tar.bz2

# macros
Source10: macros.qt5-qtwebengine

# fix extractCFlag to also look in QMAKE_CFLAGS_RELEASE, needed to detect the
# ARM flags with our %%qmake_qt5 macro, including for the next patch
Patch2:  qtwebengine-opensource-src-5.12.4-fix-extractcflag.patch
# disable NEON vector instructions on ARM where the NEON code FTBFS due to
# GCC bug https://bugzilla.redhat.com/show_bug.cgi?id=1282495
Patch3:  qtwebengine-opensource-src-5.9.0-no-neon.patch
# workaround FTBFS against kernel-headers-5.2.0+
Patch4:  qtwebengine-SIOCGSTAMP.patch
#  fix build when using qt < 5.14
Patch5:  qtwebengine-5.15.0-QT_DEPRECATED_VERSION.patch
# gcc-12 FTBFS "use of deleted function"
Patch6:  chromium-angle-nullptr.patch
Patch7:  chromium-hunspell-nullptr.patch
#Patch8:  qtwebengine-everywhere-5.15.8-libpipewire-0.3.patch
# Fix/workaround FTBFS on aarch64 with newer glibc
Patch24: qtwebengine-everywhere-src-5.11.3-aarch64-new-stat.patch
# Use Python2
Patch26: qtwebengine-everywhere-5.15.5-use-python2-main-tree.patch
#Patch27: qtwebengine-everywhere-5.15.5-use-python2-chromium.patch

Patch32: qtwebengine-skia-missing-includes.patch
# Fix QtWebEngine on Apple M1 hardware (patch from Arch Linux ARM)
## Cf. https://bugreports.qt.io/browse/QTBUG-108674
## Cf. https://bugzilla.redhat.com/show_bug.cgi?id=2144200
## From: https://chromium-review.googlesource.com/c/chromium/src/+/3545665
#Patch33: qtwebengine-5.15-Backport-of-16k-page-support-on-aarch64.patch
#Patch34: qtwebengine-fix-build-chromium.patch
Patch35: qt5-qtwebengine-c99.patch
Patch36: qtwebengine-fix-build-main-tree.patch

BuildRequires: make
BuildRequires: python
BuildRequires: opt-qt5-qtbase-devel
BuildRequires: opt-qt5-qtbase-private-devel
BuildRequires: opt-qt5-qtdeclarative-devel
BuildRequires: opt-qt5-qtxmlpatterns-devel
BuildRequires: opt-qt5-qtlocation-devel
BuildRequires: opt-qt5-qtsensors-devel
BuildRequires: opt-qt5-qtsvg-devel
BuildRequires: opt-qt5-qtwebchannel-devel
BuildRequires: opt-qt5-qttools-static
BuildRequires: opt-qt5-qtquickcontrols2-devel
BuildRequires: ninja
BuildRequires: cmake
BuildRequires: bison
BuildRequires: flex
BuildRequires: gcc-c++
# gn links statically (for now)
BuildRequires: libstdc++-static
BuildRequires: git-core
BuildRequires: gperf
%if 0%{?use_system_libicu}
BuildRequires: libicu-devel >= 65
%endif
BuildRequires: libjpeg-devel
BuildRequires: nodejs18
%if 0%{?use_system_re2}
BuildRequires: re2-devel
%endif
%if 0%{?pipewire}
BuildRequires:  pkgconfig(libpipewire-0.3)
%endif
#BuildRequires: snappy-devel
BuildRequires: pkgconfig(expat)
BuildRequires: pkgconfig(gobject-2.0)
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(fontconfig)
BuildRequires: pkgconfig(freetype2)
#BuildRequires: pkgconfig(gl)
BuildRequires: pkgconfig(egl)
%if 0%{?use_system_jsoncpp}
BuildRequires: pkgconfig(jsoncpp)
%endif
BuildRequires: pkgconfig(libpng)
BuildRequires: pkgconfig(libudev)
%if 0%{?use_system_libwebp}
BuildRequires: pkgconfig(libwebp) >= 0.6.0
%endif
BuildRequires: pkgconfig(harfbuzz)
BuildRequires: pkgconfig(libdrm)
BuildRequires: pkgconfig(opus)

# SFOS replacement
#BuildRequires: pkgconfig(libevent)
BuildRequires: libev-libevent-devel

BuildRequires: pkgconfig(poppler-cpp)
BuildRequires: pkgconfig(zlib)
%if 0%{?fedora} && 0%{?fedora} < 30
BuildRequires: pkgconfig(minizip)
%else
BuildConflicts: minizip-devel
Provides: bundled(minizip) = 1.2
%endif
#BuildRequires: pkgconfig(x11)
#BuildRequires: pkgconfig(xi)
#BuildRequires: pkgconfig(xcursor)
#BuildRequires: pkgconfig(xext)
#BuildRequires: pkgconfig(xfixes)
#BuildRequires: pkgconfig(xrender)
#BuildRequires: pkgconfig(xdamage)
#BuildRequires: pkgconfig(xcomposite)
#BuildRequires: pkgconfig(xtst)
#BuildRequires: pkgconfig(xrandr)
#BuildRequires: pkgconfig(xscrnsaver)
BuildRequires: pkgconfig(libcap)
BuildRequires: pkgconfig(libpulse)
BuildRequires: pkgconfig(alsa)
#BuildRequires: pkgconfig(libpci)
BuildRequires: pkgconfig(dbus-1)
BuildRequires: pkgconfig(nss)
#BuildRequires: pkgconfig(lcms2)
BuildRequires: pkgconfig(xkbcommon)
#BuildRequires: pkgconfig(xkbfile)
## https://bugreports.qt.io/browse/QTBUG-59094
## requires libxml2 built with icu support
#BuildRequires: pkgconfig(libxslt) pkgconfig(libxml-2.0)
BuildRequires: perl
# fesco exception to allow python2 use: https://pagure.io/fesco/issue/2208
# per https://fedoraproject.org/wiki/Changes/RetirePython2#FESCo_exceptions
# Only the interpreter is needed
%if 0%{?use_system_libvpx}
BuildRequires: pkgconfig(vpx) >= 1.8.0
%endif

%{?_opt_qt5_version:Requires: opt-qt5-qtbase%{?_isa} = %{_opt_qt5_version}}
Requires: opt-qt5-qtlocation >= %{qt_version}
Requires: opt-qt5-qtbase-gui >= %{qt_version}
Requires: opt-qt5-qtdeclarative >= %{qt_version}
Requires: opt-qt5-qtwebchannel >= %{qt_version}
Requires: opt-qt5-qtsensors >= %{qt_version}
Requires: opt-qt5-qtsensors >= %{qt_version}
Requires: opt-qt5-qtsvg >= %{qt_version}

%description
%{summary}.

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: opt-qt5-qtbase-devel%{?_isa}
Requires: opt-qt5-qtdeclarative-devel%{?_isa}
# not arch'd for now, see if can get away with avoiding multilib'ing -- rex
Requires: %{name}-devtools = %{version}-%{release}
%description devel
%{summary}.

%package devtools
Summary: WebEngine devtools_resources
Requires: %{name}%{?_isa} = %{version}-%{release}
%description devtools
Support for remote debugging.

%package designer-plugin
Summary: WebEngine Designer plugin
Requires: %{name}%{?_isa} = %{version}-%{release}
%description designer-plugin
Support for Designer.


%prep
%setup -n %{name}-%{version}/upstream

# SB2 refuses to patch across the submodules. So, we have to split the
# patches

# patches in main src
%patch2 -p1
%patch3 -p1
%patch5 -p1
%patch26 -p1
%patch36 -p1

# patches in src/3rdparty
pushd src/3rdparty
%patch4 -p3
%patch6 -p3
%patch7 -p3
%patch24 -p3
#%patch27 -p3
%patch32 -p3
#%patch33 -p3
#%patch34 -p3
%patch35 -p3
popd

# copy the Chromium license so it is installed with the appropriate name
cp -p src/3rdparty/chromium/LICENSE LICENSE.Chromium

# consider doing this as part of the tarball creation step instead?  rdieter
# fix/workaround
# fatal error: QtWebEngineCore/qtwebenginecoreglobal.h: No such file or directory
if [ ! -f "./include/QtWebEngineCore/qtwebenginecoreglobal.h" ]; then
%_opt_qt5_bindir/syncqt.pl -version %{version}
fi

# abort if this doesn't get created by syncqt.pl
test -f "./include/QtWebEngineCore/qtwebenginecoreglobal.h"


%build
export QTDIR=%{_opt_qt5_prefix}
touch .git

export STRIP=strip
export NINJAFLAGS="%{__ninja_common_opts}"
export NINJAJOBS=%{?_smp_mflags}
export NINJA_PATH=%{__ninja}

%{opt_qmake_qt5} \
  CONFIG+="link_pulseaudio use_gold_linker" \
  %{?use_system_libicu:QMAKE_EXTRA_ARGS+="-system-webengine-icu"} \
  QMAKE_EXTRA_ARGS+=" -webengine-proprietary-codecs" \
  QMAKE_STRIP=$STRIP \
  .

# avoid %%make_build for now, the -O flag buffers output from intermediate build steps done via ninja
make %{?_smp_mflags}

%install
make install INSTALL_ROOT=%{buildroot}

# rpm macros
install -p -m644 -D %{SOURCE10} \
  %{buildroot}%{rpm_macros_dir}/macros.qt5-qtwebengine
sed -i \
  -e "s|@@NAME@@|%{name}|g" \
  -e "s|@@EPOCH@@|%{?epoch}%{!?epoch:0}|g" \
  -e "s|@@VERSION@@|%{version}|g" \
  -e "s|@@EVR@@|%{?epoch:%{epoch:}}%{version}-%{release}|g" \
  %{buildroot}%{rpm_macros_dir}/macros.qt5-qtwebengine

## .prl/.la file love
# nuke .prl reference(s) to %%buildroot, excessive (.la-like) libs
pushd %{buildroot}%{_opt_qt5_libdir}
for prl_file in libQt5*.prl ; do
  sed -i -e "/^QMAKE_PRL_BUILD_DIR/d" ${prl_file}
  if [ -f "$(basename ${prl_file} .prl).so" ]; then
    rm -fv "$(basename ${prl_file} .prl).la"
    sed -i -e "/^QMAKE_PRL_LIBS/d" ${prl_file}
  fi
done
# explicitly omit, at least until there's a real library installed associated with it -- rex
rm -fv Qt5WebEngineCore.la
popd

mkdir -p %{buildroot}%{_qtwebengine_dictionaries_dir}

# adjust cmake dep(s) to allow for using the same Qt5 that was used to build it
# using the lesser of %%version, %%_qt5_version
%global lesser_version $(echo -e "%{version}\\n%{qt_version}" | sort -V | head -1)
sed -i -e "s|%{qt_webengine_version} \${_Qt5WebEngine|%{lesser_version} \${_Qt5WebEngine|" \
  %{buildroot}%{_opt_qt5_libdir}/cmake/Qt5WebEngine*/Qt5WebEngine*Config.cmake

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%license LICENSE.*
%if 0%{?docs}
%license src/webengine/doc/src/qtwebengine-3rdparty.qdoc
%endif
%{_opt_qt5_libdir}/libQt5*.so.*
%{_opt_qt5_bindir}/qwebengine_convert_dict
%{_opt_qt5_libdir}/qt5/qml/*
%{_opt_qt5_libdir}/qt5/libexec/QtWebEngineProcess
%{_opt_qt5_plugindir}/imageformats/libqpdf.so
%dir %{_opt_qt5_datadir}/resources/
%if ! 0%{?use_system_libicu}
%{_opt_qt5_datadir}/resources/icudtl.dat
%endif
%{_opt_qt5_datadir}/resources/qtwebengine_resources_100p.pak
%{_opt_qt5_datadir}/resources/qtwebengine_resources_200p.pak
%{_opt_qt5_datadir}/resources/qtwebengine_resources.pak
%dir %{_qtwebengine_dictionaries_dir}
%dir %{_opt_qt5_translationdir}/qtwebengine_locales
%lang(am) %{_opt_qt5_translationdir}/qtwebengine_locales/am.pak
%lang(ar) %{_opt_qt5_translationdir}/qtwebengine_locales/ar.pak
%lang(bg) %{_opt_qt5_translationdir}/qtwebengine_locales/bg.pak
%lang(bn) %{_opt_qt5_translationdir}/qtwebengine_locales/bn.pak
%lang(ca) %{_opt_qt5_translationdir}/qtwebengine_locales/ca.pak
%lang(cs) %{_opt_qt5_translationdir}/qtwebengine_locales/cs.pak
%lang(da) %{_opt_qt5_translationdir}/qtwebengine_locales/da.pak
%lang(de) %{_opt_qt5_translationdir}/qtwebengine_locales/de.pak
%lang(el) %{_opt_qt5_translationdir}/qtwebengine_locales/el.pak
%lang(en) %{_opt_qt5_translationdir}/qtwebengine_locales/en-GB.pak
%lang(en) %{_opt_qt5_translationdir}/qtwebengine_locales/en-US.pak
%lang(es) %{_opt_qt5_translationdir}/qtwebengine_locales/es-419.pak
%lang(es) %{_opt_qt5_translationdir}/qtwebengine_locales/es.pak
%lang(et) %{_opt_qt5_translationdir}/qtwebengine_locales/et.pak
%lang(fa) %{_opt_qt5_translationdir}/qtwebengine_locales/fa.pak
%lang(fi) %{_opt_qt5_translationdir}/qtwebengine_locales/fi.pak
%lang(fil) %{_opt_qt5_translationdir}/qtwebengine_locales/fil.pak
%lang(fr) %{_opt_qt5_translationdir}/qtwebengine_locales/fr.pak
%lang(gu) %{_opt_qt5_translationdir}/qtwebengine_locales/gu.pak
%lang(he) %{_opt_qt5_translationdir}/qtwebengine_locales/he.pak
%lang(hi) %{_opt_qt5_translationdir}/qtwebengine_locales/hi.pak
%lang(hr) %{_opt_qt5_translationdir}/qtwebengine_locales/hr.pak
%lang(hu) %{_opt_qt5_translationdir}/qtwebengine_locales/hu.pak
%lang(id) %{_opt_qt5_translationdir}/qtwebengine_locales/id.pak
%lang(it) %{_opt_qt5_translationdir}/qtwebengine_locales/it.pak
%lang(ja) %{_opt_qt5_translationdir}/qtwebengine_locales/ja.pak
%lang(kn) %{_opt_qt5_translationdir}/qtwebengine_locales/kn.pak
%lang(ko) %{_opt_qt5_translationdir}/qtwebengine_locales/ko.pak
%lang(lt) %{_opt_qt5_translationdir}/qtwebengine_locales/lt.pak
%lang(lv) %{_opt_qt5_translationdir}/qtwebengine_locales/lv.pak
%lang(ml) %{_opt_qt5_translationdir}/qtwebengine_locales/ml.pak
%lang(mr) %{_opt_qt5_translationdir}/qtwebengine_locales/mr.pak
%lang(ms) %{_opt_qt5_translationdir}/qtwebengine_locales/ms.pak
%lang(nb) %{_opt_qt5_translationdir}/qtwebengine_locales/nb.pak
%lang(nl) %{_opt_qt5_translationdir}/qtwebengine_locales/nl.pak
%lang(pl) %{_opt_qt5_translationdir}/qtwebengine_locales/pl.pak
%lang(pt_BR) %{_opt_qt5_translationdir}/qtwebengine_locales/pt-BR.pak
%lang(pt_PT) %{_opt_qt5_translationdir}/qtwebengine_locales/pt-PT.pak
%lang(ro) %{_opt_qt5_translationdir}/qtwebengine_locales/ro.pak
%lang(ru) %{_opt_qt5_translationdir}/qtwebengine_locales/ru.pak
%lang(sk) %{_opt_qt5_translationdir}/qtwebengine_locales/sk.pak
%lang(sl) %{_opt_qt5_translationdir}/qtwebengine_locales/sl.pak
%lang(sr) %{_opt_qt5_translationdir}/qtwebengine_locales/sr.pak
%lang(sv) %{_opt_qt5_translationdir}/qtwebengine_locales/sv.pak
%lang(sw) %{_opt_qt5_translationdir}/qtwebengine_locales/sw.pak
%lang(ta) %{_opt_qt5_translationdir}/qtwebengine_locales/ta.pak
%lang(te) %{_opt_qt5_translationdir}/qtwebengine_locales/te.pak
%lang(th) %{_opt_qt5_translationdir}/qtwebengine_locales/th.pak
%lang(tr) %{_opt_qt5_translationdir}/qtwebengine_locales/tr.pak
%lang(uk) %{_opt_qt5_translationdir}/qtwebengine_locales/uk.pak
%lang(vi) %{_opt_qt5_translationdir}/qtwebengine_locales/vi.pak
%lang(zh_CN) %{_opt_qt5_translationdir}/qtwebengine_locales/zh-CN.pak
%lang(zh_TW) %{_opt_qt5_translationdir}/qtwebengine_locales/zh-TW.pak

%files devel
%{rpm_macros_dir}/macros.qt5-qtwebengine
%{_opt_qt5_headerdir}/Qt*/
%{_opt_qt5_libdir}/libQt5*.so
%{_opt_qt5_libdir}/libQt5*.prl
%{_opt_qt5_libdir}/cmake/Qt5*/
%{_opt_qt5_libdir}/pkgconfig/Qt5*.pc
%{_opt_qt5_archdatadir}/mkspecs/modules/*.pri

%files devtools
%{_opt_qt5_datadir}/resources/qtwebengine_devtools_resources.pak

%files designer-plugin
%{_opt_qt5_plugindir}/designer/libqwebengineview.so
