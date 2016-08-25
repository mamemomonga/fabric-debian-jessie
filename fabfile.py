# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8

from fabric.api import *
from fabric.contrib.files import *

@task
def setup():

	# SSH公開鍵を登録する
	import os
	sshdir='/home/'+env.user+'/.ssh'
	if not exists(sshdir):
		run('mkdir '+sshdir)
		run('chmod 755 '+sshdir)
		append( sshdir+'/authorized_keys', open( os.environ['HOME']+"/.ssh/id_rsa.pub" ).read().rstrip())
		run('chmod 644 '+sshdir+'/authorized_keys')

	# sudo を登録する
	if not exists("/etc/sudoers.d/wheel"):
		print "root password"

		run("""
su -c 'DEBIAN_FRONTEND=noninteractive apt-get install -y sudo && \\
  echo "%(USER)s ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/wheel && \\
  chmod 600 /etc/sudoers.d/wheel
'""" % { 'USER' : env.user })

	# sshd
	comment('/etc/ssh/sshd_config','^PermitRootLogin without-password',char='# ',use_sudo=True)
	append( '/etc/ssh/sshd_config','PermitRootLogin no',use_sudo=True)
	append( '/etc/ssh/sshd_config','PasswordAuthentication no',use_sudo=True)

	# ロケール
	sudo("uname -a")
	# uncomment('/etc/locale.gen','^# en_US.UTF-8 UTF-8',char='# ',use_sudo=True)
	# uncomment('/etc/locale.gen','^# ja_JP.UTF-8 UTF-8',char='# ',use_sudo=True)
	sudo('locale-gen')
	# append('/etc/bash.bashrc','LC_MESSAGES=en_US.UTF-8',use_sudo=True)
	sudo("update-locale LANG=C")

	# アップデート
	# libpam-systemd を入れればsshdからshutdownしても固まらない
	# http://symfoware.blog68.fc2.com/blog-entry-1734.html

	sudo('DEBIAN_FRONTEND=noninteractive apt-get install -y aptitude libpam-systemd')
	sudo('aptitude update')
	sudo('DEBIAN_FRONTEND=noninteractive aptitude -y upgrade')

	dnssd()
	vim()

	# うまくいかないのでsshコマンド経由でreboot
	# rebootコマンドは作り直す必要があるようだ
	local("ssh %s@%s 'sudo reboot'; exit 0" % ( env.user, env.host_string) )

@task
def dnssd():
    sudo('DEBIAN_FRONTEND=noninteractive aptitude install -y avahi-daemon libnss-mdns')
    if not exists('/etc/avahi/services/ssh.service'):
        append('/etc/avahi/services/ssh.service',"""
<?xml version="1.0" standalone='no'?>
<!DOCTYPE service-group SYSTEM "avahi-service.dtd">
<service-group>
  <name replace-wildcards="yes">%h</name>
  <service>
    <type>_ssh._tcp</type>
    <port>22</port>
  </service>
</service-group>
""",use_sudo=True);

@task
def vim():
    sudo('DEBIAN_FRONTEND=noninteractive aptitude install -y vim')

    if not exists('/root/.vimrc'):
        append('/root/.vimrc',"""
syntax on
set wildmenu
set history=100
set number
set scrolloff=5
set autowrite
set tabstop=4
set shiftwidth=4
set softtabstop=0
set termencoding=utf-8
set encoding=utf-8
set fileencodings=iso-2022-jp,utf-8,cp932,euc-jp,ucs2le,ucs-2
set fenc=utf-8
set enc=utf-8
""",use_sudo=True)

    sudo('cp /root/.vimrc /etc/skel/.vimrc')
    sudo('echo "3" | update-alternatives --config editor')

