# encoding: UTF-8

require 'chef'
require 'chefspec'
require 'chefspec/berkshelf'
require 'chefspec/deprecations'

::RHEL_OPTS = {
  platform: 'redhat',
  version: '6.3'
}
DEBIAN_OPTS = {
  platform: 'ubuntu',
  version: '12.04'
}
