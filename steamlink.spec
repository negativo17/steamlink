# Remove bundled libraries from requirements/provides
%global __requires_exclude ^(libavcodec\\.so.*|libavutil\\.so.*|libKF5DBusAddons\\.so.*|libQt5.*\\.so.*|libSDL2.*\\.so.*|libSDL3.*\\.so.*)$
%global __provides_exclude ^(libavcodec\\.so.*|libavutil\\.so.*|libKF5DBusAddons\\.so.*|libQt5.*\\.so.*|libSDL2.*\\.so.*|libSDL3.*\\.so.*)$
%global __requires_exclude_from ^%{_libdir}/%{name}/lib/plugins/.*$
%global __provides_exclude_from ^%{_libdir}/%{name}/lib/plugins/.*$

%global desktop_id com.valvesoftware.SteamLink

Name:           steamlink
Version:        1.3.10.259
Release:        1%{?dist}
Summary:        Stream games from another computer with Steam
License:        Steamlink License
URL:            https://store.steampowered.com/app/353380/Steam_Link/

# Content of the flatpak (https://flathub.org/apps/com.valvesoftware.SteamLink):
Source0:        %{name}-%{version}-x86_64.tar.xz
Source1:        %{name}-wrapper

BuildRequires:  chrpath
BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib
BuildRequires:  sed

Requires:       hicolor-icon-theme
Requires:       steam-devices

%description
The Steam Link app allows you to stream games from your other computers. Just
plug in a controller, connect to a computer running Steam on the same local
network, and start playing your existing Steam games.

%prep
%setup -q -c
chrpath -d lib/libSDL3*

%install
# Exploded Flatpak contents
mkdir -p %{buildroot}%{_libdir}/steamlink/share
cp -afr lib bin %{buildroot}%{_libdir}/steamlink/
cp -afr share/qlogging-categories5 %{buildroot}%{_libdir}/steamlink/share/
mkdir -p %{buildroot}%{_datadir}/
cp -afr share/icons share/applications %{buildroot}%{_datadir}/
cp -afr share/appdata %{buildroot}%{_metainfodir}

# Wrapper script stuff
mkdir %{buildroot}%{_bindir}
cat %{SOURCE1} | sed -e 's|INSTALL_DIR|%{_libdir}/%{name}|g' \
    > %{buildroot}%{_bindir}/%{name}
chmod +x %{buildroot}%{_bindir}/%{name}

%check
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/%{desktop_id}.appdata.xml
desktop-file-validate %{buildroot}%{_datadir}/applications/%{desktop_id}.desktop

%files
%license LICENSE.txt ThirdPartyLegalNotices.*
%doc README.txt
%{_bindir}/%{name}
%{_libdir}/steamlink/
%{_metainfodir}/%{desktop_id}.appdata.xml
%{_datadir}/applications/%{desktop_id}.desktop
%{_datadir}/icons/hicolor/256x256/apps/%{desktop_id}.png

%changelog
* Sun Aug 18 2024 Simone Caronni <negativo17@gmail.com> - 1.3.10.259-1
- First build.
