# encoding: UTF-8

require_relative 'spec_helper'

describe 'curl::libcurl' do
  let(:chef_run) do
    ChefSpec::Runner.new(DEBIAN_OPTS)
      .converge(described_recipe)
  end

  it 'installs packages' do
    %w(libcurl3 libcurl4-openssl-dev).each do |pkg|
      expect(chef_run).to upgrade_package pkg
    end
  end
end
