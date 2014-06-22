class CLI


  def load_todos
    @todo_arr = IO.readlines("todo.txt")
  end

  def print_todos
    @todo_arr.each { |e| print e }
  end

  def get_pri(pri)
    ret=[]
    @todo_arr.each do |td| 
      ret << td if td.start_with?("(#{pri.upcase})")
    end
    return ret
  end

  def parse_todos
    case ARGV[0]
    when "today"
      print "ok, today\n"
    when "ls"
      print_todos
    when "pri"
       get_pri(ARGV[1]).each do |td|
         print td
       end
    when /^add([a-d])/
      puts "add all right " + $1
    end
  end

  def run()
    load_todos
    parse_todos
  end
end
cli = CLI.new
cli.run

