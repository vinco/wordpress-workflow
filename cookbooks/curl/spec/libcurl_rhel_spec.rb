# encoding: UTF-8

require_relative 'spec_helper'

describe 'curl::libcurl' do
  let(:chef_run) do
    ChefSpec::Runner.new(RHEL_OPTS)
      .converge(described_recipe)
  end

  it 'installs package' do
    %w(curl-devel).each do |pkg|
      expect(chef_run).to upgrade_package pkg
    end
  end
end
