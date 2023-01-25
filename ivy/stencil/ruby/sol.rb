#!/usr/bin/ruby

require "open3"

if ARGV.count != 1
  print("Usage: ./sol.rb <path to ivy binary to attack>\n")
  exit(1)
end

ivy_path = ARGV[0]

Open3.popen3(ivy_path) do |IVY_STDIN, IVY_STDOUT, IVY_STDERR, _|
  #
  # TODO: Implement your attack here.
  #
  # You can send data to the STDIN of the ivy binary with the following:
  #
  #   IVY_STDIN.puts("data to send")
  #
  # You can read the next line from the ivy binary's STDOUT or STDERR with the
  # following:
  #
  #   IVY_STDOUT.gets
  #
end
