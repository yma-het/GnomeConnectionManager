Summary: A tabbed SSH connection manager for GTK+ environments
Name: gnome-connection-manager
Version: 1.2.1
Release: 1%{?dist}
License: GPLv3 and MIT
URL: http://kuthulu.com/gcm/

Source0: https://github.com/yma-het/GnomeConnectionManager/archive/v_%{version}.tar.gz

BuildArch: noarch

BuildRequires: vte
BuildRequires: python
BuildRequires: desktop-file-utils
Requires: vte
Requires: expect
Requires: pygtk2-libglade

%description
Gnome Connection Manager is a tabbed SSH connection manager for GTK+
environments.

%prep
%setup -q -c
# Remove pre-compiled files
find . -name "*.pyc" -exec rm -f {} \;
find . -name "*.pyo" -exec rm -f {} \;

# Fix shebang line
sed -i -e 's/^#!.*//' pyAES.py

%build
# Compile mo files
for po_file in $(find ./lang -name "*_*.po" -printf "%f\n"); do
    msgfmt lang/${po_file} -o lang/$(echo ${po_file} | sed "s@_..\.po@@g")/LC_MESSAGES/gcm-lang.mo
done

%install
# Install application
install -d -m 755 %{buildroot}%{_datadir}/%{name}
cp -pr *.py *.glade ssh.expect *.gif *.png *.desktop %{buildroot}%{_datadir}/%{name}

# Install icon and desktop file
install -d -m 755 %{buildroot}%{_datadir}/icons/hicolor/128x128/apps
install -p -m 644 icon.png \
  %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/%{name}.png
desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  --add-category GNOME \
  --add-category GTK \
  --add-category Utility \
  %{name}.desktop

# Install start script
install -d -m 755 %{buildroot}%{_bindir}
install -p -m 755 %{name}.sh %{buildroot}%{_bindir}/%{name}

# Install appdata
install -d -m 755 %{buildroot}%{_datadir}/appdata
install -p -m 644 %{name}.appdata.xml %{buildroot}%{_datadir}/appdata/%{name}.appdata.xml

# Install locales
install -d -m 755 %{buildroot}%{_datadir}/locale
cp -r  lang/ %{buildroot}%{_datadir}/%{name} 
cp -pr lang/?? %{buildroot}%{_datadir}/locale
%find_lang gcm-lang

%post
touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
  %{_bindir}/gtk-update-icon-cache -q %{_datadir}/icons/hicolor
fi

%postun
touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
  %{_bindir}/gtk-update-icon-cache -q %{_datadir}/icons/hicolor
fi

%files -f gcm-lang.lang
%doc LICENSES
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_datadir}/icons/hicolor/128x128/apps/%{name}.png
%{_datadir}/applications/%{name}.desktop
%{_datadir}/appdata/%{name}.appdata.xml

%changelog
* Sat Feb 07 2019 Yury Molodtsov <yma.het@gmail.com> - 1.2.1-1
- Added fullscreen mode
- Added ability to chose custom ssh binary
- Removed plain function keys shortcuts
- Corrected locales compilation
- Rewrited spec to work from git repo

* Thu Nov 06 2014 Mat Booth <mat.booth@redhat.com> - 1.1.0-4
- Add appstream appdata.
- Install locales correctly.

* Wed Feb 27 2013 Mat Booth <mbooth@fedoraproject.org> 1.1.0-3
- Add BR/R on vte.

* Mon Feb 11 2013 Mat Booth <mbooth@fedoraproject.org> 1.1.0-2
- Include expect script.
- Add MIT license for AES impl.

* Mon Feb 11 2013 Mat Booth <mbooth@fedoraproject.org> 1.1.0-1
- Initial spec file.

