%global debug_package %{nil}

# Exclude private libraries
%global __requires_exclude ^(libavcodec\\.so\\.61.*|libavutil\\.so\\.59.*|libQt6Core\\.so\\.6.*|libQt6Gui\\.so\\.6.*|libQt6Network\\.so\\.6.*|libQt6Widgets\\.so\\.6.*|libSDL3_mixer\\.so\\.0.*|libsteamwebrtc\\.so.*|libvpx\\.so\\.6.*)$
%global __provides_exclude_from ^%{_libdir}/%{name}/lib/.*$

%global desktop_id com.valvesoftware.SteamLink

Name:           steamlink
Version:        1.3.32.316
Release:        1%{?dist}
Summary:        Stream games from another computer with Steam
License:        Steamlink License
URL:            https://store.steampowered.com/app/353380/Steam_Link/
ExclusiveArch:  x86_64

Source0:        https://repo.steampowered.com/steamlink/%{version}/%{name}-%{version}.tgz
Source1:        %{name}-wrapper

# Valve does not ship desktop integration outside of the Flatpak:
# https://github.com/flathub/com.valvesoftware.SteamLink
%global flathub https://raw.githubusercontent.com/flathub/%{desktop_id}/refs/heads/beta
Source2:        %{flathub}/%{desktop_id}.desktop
Source3:        %{flathub}/%{desktop_id}.metainfo.xml
Source4:        %{flathub}/icons/256/%{name}.png

BuildRequires:  chrpath
BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib
BuildRequires:  sed

Requires:       hicolor-icon-theme
Requires:       steamlink-qtbase%{?_isa}
Requires:       steam-devices

%description
The Steam Link app allows you to stream games from your other computers. Just
plug in a controller, connect to a computer running Steam on the same local
network, and start playing your existing Steam games.

%prep
%autosetup -n package

# Use the system libraries where possible
rm -f \
    lib/libSDL2_ttf* \
    lib/libSDL3.so.* \
    lib/libSDL3_image.so.* \
    lib/libSDL3_ttf.so.*

# Leftover RPATH from Valve's build host
chrpath -d bin/%{name} lib/libSDL3_mixer.so.0

%install
install -p -m 0755 -D bin/%{name} %{buildroot}%{_libdir}/%{name}/bin/%{name}
install -p -m 0755 -t %{buildroot}%{_libdir}/%{name}/lib -D lib/*.so*

mkdir -p %{buildroot}%{_bindir}
sed -e 's|INSTALL_DIR|%{_libdir}/%{name}|g' %{SOURCE1} \
    > %{buildroot}%{_bindir}/%{name}
chmod 0755 %{buildroot}%{_bindir}/%{name}

install -p -m 0644 -D %{SOURCE2} %{buildroot}%{_datadir}/applications/%{desktop_id}.desktop
install -p -m 0644 -D %{SOURCE3} %{buildroot}%{_metainfodir}/%{desktop_id}.metainfo.xml
install -p -m 0644 -D %{SOURCE4} %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/%{desktop_id}.png

# Update desktop file for wrapper instead of flatpak
sed -i -e 's|Exec=/app/bin/%{name}|Exec=%{_bindir}/%{name}|g' \
    %{buildroot}%{_datadir}/applications/%{desktop_id}.desktop

%check
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/%{desktop_id}.metainfo.xml
desktop-file-validate %{buildroot}%{_datadir}/applications/%{desktop_id}.desktop

%files
%license LICENSE.txt ThirdPartyLegalNotices.*
%doc README.txt
%{_bindir}/%{name}
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/bin/
%{_libdir}/%{name}/lib/
%{_datadir}/applications/%{desktop_id}.desktop
%{_datadir}/icons/hicolor/256x256/apps/%{desktop_id}.png
%{_metainfodir}/%{desktop_id}.metainfo.xml

%changelog
* Sun Aug 23 2026 Simone Caronni <negativo17@gmail.com> - 1.3.32.316-1
- Update to 1.3.32.316.
- Use upstream tarball.
- Get the Qt 6 base libraries from steamlink-qtbase.

* Tue Sep 03 2024 Simone Caronni <negativo17@gmail.com> - 1.3.10.259-2
- Fix desktop exec line.

* Sun Aug 18 2024 Simone Caronni <negativo17@gmail.com> - 1.3.10.259-1
- First build.
