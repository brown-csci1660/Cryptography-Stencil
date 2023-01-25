#!/usr/bin/ruby

require 'socket'
# TODO: Add other imports here if necessary.

class PaddingServer
  # NOTE: You do not need to modify this function.
  def initialize(host, port)
    @host = host
    @port = port
    @sock = 0
  end

  # NOTE: You do not need to modify this function.
  def connect
    begin
      @sock = TCPSocket.new(@host, @port)
    rescue
      puts "error: #{$!}"
    end
  end

  # NOTE: You do not need to modify this function.
  def close
    @sock.close()
  end

  def send(msg)
    # Sends msg to the server.

    # TODO: Use the socket (@sock) to send the message in the `msg` variable
    # over the wire.
    #
    # Example: @sock.puts "message goes here"
    #          This will send "message goes here\n" (note the automatically
    #          added newline) to the server.
  @sock.puts "testing"
  end

  def recv
    # Reads data from the server.

    # TODO: Use the socket (@sock) to read data from the wire.
    #
    # Example: @sock.gets
    #          This will read up to the next newline sent from the server.
    return ""
  end
end

def sendCommand(host, port, cmd)
  p = PaddingServer.new(host, port)
  p.connect()

  # TODO: Implement an attack on the server that takes advantage of the padding
  # leak to send the command in `cmd` to the server using `p.send` and
  # `p.recv`.

  p.close()
end

# NOTE: You do not need to modify this function.
def main()
  if ARGV.length != 3
    STDERR.puts "Usage: #{$0} <host> <port> <command>"
    exit(1)
  end

  host = ARGV[0]
  port = ARGV[1].to_i
  commandToRun = ARGV[2]

  sendCommand(host, port, commandToRun)
end

# Run the script:
main()
