%define debug_package %{nil}

%global commit             f9cb0b066498d26a90fd918fe265adbb0ea02bcf
%global shortcommit        %(c=%{commit}; echo ${c:0:7})

Name:	        go-server-starter
Version:	0.0.2
Release:	1.1.git%{shortcommit}%{?dist}
Summary:	Go port of start_server utility (a.k.a. Server::Starter).

Group:		System Environment/Daemons
License:	MIT
URL:		https://github.com/lestrrat/go-server-starter

# Source0 tarball file %{name}.tar.gz was created with the following commands.
#
# mkdir -p go-server-starter/go/src/github.com/lestrrat
# cd go-server-starter/go
# export GOPATH=$PWD
# cd src/github.com/lestrrat
# git clone https://github.com/lestrrat/go-server-starter
# cd go-server-starter
# git checkout f9cb0b066498d26a90fd918fe265adbb0ea02bcf
# go get -d ./...
# cd $GOPATH/../..
# tar cf - go-server-starter | gzip -9 > go-server-starter.tar.gz
Source0:	%{name}.tar.gz

BuildRoot:      %{name}
BuildRequires:  golang >= 1.8

%description
The start_server utility is a superdaemon for hot-deploying server programs.

It is often a pain to write a server program that supports graceful restarts,
with no resource leaks. Server::Starter solves the problem by splitting the
task into two: start_server works as a superdaemon that binds to zero or more
TCP ports or unix sockets, and repeatedly spawns the server program that
actually handles the necessary tasks (for example, responding to incoming
connections). The spawned server programs under start_server call accept(2) and
handle the requests.

To gracefully restart the server program, send SIGHUP to the superdaemon. The
superdaemon spawns a new server program, and if (and only if) it starts up
successfully, sends SIGTERM to the old server program.

By using start_server it is much easier to write a hot-deployable server.
Following are the only requirements a server program to be run under
start_server should conform to:

receive file descriptors to listen to through an environment variable - perform
a graceful shutdown when receiving SIGTERM Many PSGI servers support this. If
you want your Go program to support it, you can look under the listener
directory for an implementation that also fills the net.Listener interface.

%prep
%setup -n %{name}

%build
export GOPATH=%{_builddir}/%{name}/go
cd %{_builddir}/%{name}/go/src/github.com/lestrrat/%{name}
go install ./...

%install
%{__rm} -rf %{buildroot}
%{__install} -pD -m 755 "%{_builddir}/%{name}/go/bin/start_server" %{buildroot}%{_bindir}/start_server

%files
%defattr(0755,root,root,-)
%{_bindir}/start_server

%changelog
* Fri Jun  9 2017 <hnakamur@gmail.com> - 0.0.2-1.1.f9cb0b0
- Initial release
